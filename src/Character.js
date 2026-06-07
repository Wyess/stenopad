export class Character {
    /**
     * @param {string} name - 文字名 (e.g., "Ka", "Ta")
     * @param {Object} sh - データベース全体 (sh['character'], sh['dictionary']等を含む)
     */
    constructor(name, sh) {
        this._name = name;
        this.prev = null;
        this.next = null;
        this.sh = sh;

        try {
            this.char = sh['character'][name];
            if (!this.char) throw new Error();
        } catch (e) {
            // セーフティフォールバック
            console.log(sh);
            console.log(name);
            this.char = sh['character']['Null'] || { default_glyph: { dx: 0, dy: 0, left: 0, right: 0, top: 0, bottom: 0, ascent: 0, path: [] } };
        }

        // 初期グリフをデフォルトに設定
        this.glyph = this.char['default_glyph'];
        this.x = 0;
        this.y = 0;
    }

    setPos(x, y) {
        this.x = x;
        this.y = y;
    }

    // --- Python側の @property 拡張群を完璧にシミュレート ---
    get dx() { return this.glyph['dx'] || 0; }
    get dy() { return this.glyph['dy'] || 0; }
    get right() { return this.glyph['right'] || 0; }
    get left() { return this.glyph['left'] || 0; }
    get top() { return this.glyph['top'] || 0; }
    get bottom() { return this.glyph['bottom'] || 0; }
    get ascent() { return this.glyph['ascent'] || 0; }

    get exit() {
        return [this.x + this.dx, this.y + this.dy];
    }

    get name() {
        return this._name;
    }

    get isMarker() {
        return 'mark' in this.tag;
    }

    get isSpace() {
        return 'space' in this.tag;
    }

    get isNewline() {
        return 'newline' in this.tag;
    }

    get path() {
        return this.paths[0];
    }

    get paths() {
        return this.glyph['path'] || [];
    }

    get clipPaths() {
        return this.glyph['clip_path'] || [];
    }

    get mask() {
        return this.glyph['mask'] || [];
    }

    get lengths() {
        return this.paths.map(p => p['length'] || 0);
    }

    get tag() {
        try {
            return this.sh['character'][this.name]['tag'] || {};
        } catch (e) {
            return {};
        }
    }

    get glyphs() {
        try {
            return this.sh['character'][this.name]['glyphs'] || [];
        } catch (e) {
            return [];
        }
    }

    /**
     * 収束ループ用のグリフ選択メソッド
     * 状態に変化があった場合のみ true を返す
     */
    selectGlyph() {
        for (const glyph of this.glyphs) {
            // 条件キー("key")が設定されており、それが真と評価された場合
            if (glyph['key'] && glyph['key'] !== "default") {
                if (this._evaluateSelector(glyph['key'])) {
                    const changed = (this.glyph !== glyph);
                    this.glyph = glyph;
                    return changed; // 変化フラグを返す
                }
            }
        }

        // 条件がどれも合わない場合は default_glyph に戻る
        const defaultGlyph = this.char['default_glyph'];
        const changed = (this.glyph !== defaultGlyph);
        this.glyph = defaultGlyph;
        return changed;
    }

    // --- セレクタ式評価エンジン (以前Okを実証したコードの統合版) ---
    _evaluateSelector(selectorStr) {
        if (!selectorStr || selectorStr.trim() === "" || selectorStr === "default") return true;

        const tokenRegex = /\||\.|!|\(|\)|[a-z@][a-z0-9_]*\[-?\d+(?::-?\d+)?\]/g;
        const tokens = selectorStr.match(tokenRegex) || [];
        let tokenIndex = 0;

        const peek = () => tokens[tokenIndex];
        const consume = () => tokens[tokenIndex++];

        const parseOr = () => {
            let result = parseAnd();
            while (peek() === '|') { consume(); const right = parseAnd(); result = result || right; }
            return result;
        };

        const parseAnd = () => {
            let result = parseNot();
            while (peek() === '.') { consume(); const right = parseNot(); result = result && right; }
            return result;
        };

        const parseNot = () => {
            if (peek() === '!') { consume(); return !parsePrimary(); }
            return parsePrimary();
        };

        const parsePrimary = () => {
            const token = peek();
            if (token === '(') {
                consume();
                const result = parseOr();
                if (peek() === ')') consume();
                return result;
            }
            if (token && token !== ')' && token !== '|' && token !== '.') {
                consume();
                return this._evalAtom(token);
            }
            return false;
        };

        try {
            return parseOr();
        } catch (e) {
            return false;
        }
    }
    /**
     * 隣人のタグ、または【選択されたグリフが持つタグ】を動的に判定
     */
    _evalAtom(atomToken) {
        const match = atomToken.match(/^([a-z@][a-z0-9_]*)\[(-?\d+)\]$/);
        if (!match) return false;

        const tagName = match[1];
        const offset = parseInt(match[2], 10);

        // 相対位置のCharacter（隣人）を取得
        const target = this._getNeighbor(offset);
        if (!target) return false;

        // 💡 グリフ側に 'tag' プロパティが（空配列や空オブジェクトであっても）明示的に存在するかチェック
        console.log(target.glyph);
        if (target.glyph && target.glyph.tag !== undefined && target.glyph.tag !== null) {

            // 1. 配列の場合 (e.g., ["mark", "chopped"])
            if (Array.isArray(target.glyph.tag)) {
                return target.glyph.tag.includes(tagName);
            }

            // 2. オブジェクト/辞書の場合 (e.g., {"mark": true})
            if (typeof target.glyph.tag === 'object') {
                return tagName in target.glyph.tag;
            }

            // 3. 文字列の場合 (e.g., "mark")
            if (typeof target.glyph.tag === 'string') {
                return target.glyph.tag === tagName;
            }

            return false;
        }

        // 💡 グリフ側に 'tag' が定義されていない場合のみ、文字自体の固定タグを見に行く
        if (target.tag && tagName in target.tag) {
            return true;
        }

        return false;
    }

    _getNeighbor(offset) {
        if (offset === 0) return this;
        let current = this;
        const steps = Math.abs(offset);
        const direction = offset > 0 ? 'next' : 'prev';
        for (let i = 0; i < steps; i++) {
            if (!current[direction]) return null;
            current = current[direction];
        }
        return current;
    }

    // アニメーションおよびSVG要素の生成メソッド (後半の移植で利用するためガワを維持)
    wrapElementInGElement(elem) {
        return `<g transform='translate(${this.x} ${this.y})'>${elem}</g>`;
    }

    // Pythonの get_style_to_animate(length) 相当
    getStyleToAnimate(length) {
        const dash = length;
        const gap = dash + 0.1;
        const offset = dash;
        return `stroke-dasharray:${dash} ${gap}; stroke-dashoffset:${offset};`;
    }

    // Pythonの get_dashoffset_style(...) 相当
    getDashoffsetStyle(beginS, lengthMm, durationS, targetS = 0) {
        const dash = lengthMm;
        const gap = dash + 0.25;
        let offset = 0;
        if (lengthMm !== 0) {
            // 指定時刻における描画進捗率を0〜1にクランプしてオフセットを計算
            const progress = Math.max(0, Math.min(1, (beginS + durationS - targetS) / durationS));
            offset = lengthMm * progress;
        }
        return `stroke-dasharray:${dash} ${gap}; stroke-dashoffset:${offset};`;
    }

    // Pythonの create_animate_element(...) 相当
    createAnimateElement(beginS, lengthMm, speedMmPerS) {
        const dur = lengthMm / speedMmPerS;
        return `<animate attributeName="stroke-dashoffset" values="${lengthMm};0" dur="${dur}s" begin="${beginS}s" fill="freeze"/>`;
    }

    // クリップパス要素の生成（乱数ID衝突回避）
    createClipPathElements() {
        if (this.clipPaths && this.clipPaths.length > 0) {
            const id = Math.floor(Math.random() * 0x10000);
            const dStr = this.clipPaths.map(cp => cp['d']).join('');
            const elem = `<clipPath id="clip_${id}"><path d="${dStr}"/></clipPath>`;
            const attr = `clip-path="url(#clip_${id})"`;
            return [elem, attr];
        }
        return ["", ""];
    }

    // マスク要素の生成（乱数ID衝突回避）
    createMaskElements() {
        if (this.mask && this.mask.length > 0) {
            const id = Math.floor(Math.random() * 0x10000);
            let elem = `<mask id="mask_${id}" maskUnits="userSpaceOnUse">`;
            this.mask.forEach((m, i) => {
                const fill = (i === 0) ? "white" : "black";
                elem += `<path d="${m['d']}" style="stroke: none;" fill="${fill}" />`;
            });
            elem += '</mask>';
            const attr = `mask="url(#mask_${id})"`;
            return [elem, attr];
        }
        return ["", ""];
    }

    /**
     * Python版 create_path_element を完全再現
     */
    createPathElement({ timeS = 0, toAnimate = false, speedMmPerS = 20, toGenerateKeyframe = false, targetS = 0 } = {}) {
        let pathElem = "";

        const [clipPathElem, clipPathAttr] = this.createClipPathElements();
        pathElem += clipPathElem;

        const [maskElem, maskAttr] = this.createMaskElements();
        pathElem += maskElem;

        if (toAnimate) {
            // リアルタイムアニメーションモード
            for (let i = 0; i < this.paths.length; i++) {
                const path = this.paths[i];
                const length = this.lengths[i] || 0;

                const styleAttr = this.getStyleToAnimate(length);
                const animate = this.createAnimateElement(timeS, length, speedMmPerS);

                pathElem += `<path d="${path['d']}" ${clipPathAttr} ${maskAttr} style="${styleAttr}">${animate}</path>`;
                timeS += length / speedMmPerS; // 次のパスの開始時刻を進める
            }
        } else if (toGenerateKeyframe) {
            // 時刻指定コマ送り（シーク）モード
            for (let i = 0; i < this.paths.length; i++) {
                const path = this.paths[i];
                const length = this.lengths[i] || 0;
                const durationS = length / speedMmPerS;

                const styleAttr = this.getDashoffsetStyle(timeS, length, durationS, targetS);

                pathElem += `<path d="${path['d']}" ${clipPathAttr} ${maskAttr} style="${styleAttr} stroke: #000000; stroke-width: 0.425; fill: none;"></path>`;
                timeS += durationS;
            }
        } else {
            // 通常の静的描画モード
            const pathsD = this.paths.map(p => p['d']).join('');
            const styleAttr = "stroke: #000000; stroke-width: 0.425; fill: none;";
            pathElem += `<path d="${pathsD}" ${clipPathAttr} ${maskAttr} style="${styleAttr}"/>`;
        }

        pathElem = this.wrapElementInGElement(pathElem);
        return [pathElem, timeS];
    }

}


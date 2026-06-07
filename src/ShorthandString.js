import { Character } from './Character.js';
import { Context, Line, Bbox, splitAfter, pairwise } from './LayoutComponents.js';
import { parseText } from './TextParser.js'; // パーサーのインポート



export class ShorthandString {
    /**
     * @param {string} text - 入力文字列 (e.g., "がか")
     * @param {Object} sh - データベース全体 (dictionary, trie, character定義を含む)
     */
    constructor(text, sh) {
        this.text = text;
        this.sh = sh;
        
        // 1. 文字列からCharacterの配列を生成
        this.chars = this.getChars(text);
        
        // 2. 双方向リンクの構築 (マーカースキップ構造を内包)
        this.connect();
        
        // 3. グリフの動的選択 (最大10回の収束ループ)
        this.selectGlyphs();
        
        // 4. 2次元衝突回避レイアウトの実行とBboxの決定
        this.bbox = this.layout();

        // Python側の明示的なSVGテンプレート
        this.svgTemplate = (bboxJson) => `<svg
            id="svg_root"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            version="1.1"
            viewBox="${bboxJson}"
            width="${bboxJson.width}mm"
            height="${bboxJson.height}mm"
            preserveAspectRatio="xMinYMin meet"
            data-text=""
            transform="scale(1 1)"
            transform-origin="0 0"
            style="fill: none; stroke: rgb(0, 0, 0); stroke-width: 0.425197; stroke-linecap: round; stroke-linejoin: round; stroke-miterlimit: 4; stroke-opacity: 1; background-color: #f0e68c;" >
            <rect x="${bboxJson.left}" y="${bboxJson.top}" width="100%" height="100%" fill="rgb(255 255 255)" />
            {paths}</svg>`;
    }

    /**
     * 外部で定義された `parse_text` の結果をもとにCharacterを生成
     * ※お手元の環境の text_parser.js (または同等機能) と連動させてください
     */
    getChars(text) {
        const parsedWords = parseText(text, this.sh['dictionary'], this.sh['trie']);
        console.log(parsedWords);
        return parsedWords.map(word => new Character(word, this.sh));
    }

    /**
     * Pythonの connect() を100%再現
     * 通常文字同士を繋ぎ、マーカー(isMarker)のnext接続はスキップする
     */
    connect() {
        let base = null;
        for (const char of this.chars) {
            char.prev = base;
            if (char.isMarker) {
                continue;
            } else if (base) {
                base.next = char;
            }
            base = char;
        }
    }

    /**
     * Pythonの select_glyphs() を再現
     * 最大10回ループし、すべての文字のグリフ選択状態が変化しなくなるまで収束させる
     */
    selectGlyphs() {
        for (let i = 0; i < 10; i++) {
            let totalChanged = 0;
            for (const char of this.chars) {
                if (char.selectGlyph()) {
                    totalChanged += 1;
                }
            }
            // 変化した文字が0になったら定常状態に達したため終了
            if (totalChanged === 0) {
                return;
            }
        }
        throw new Error("Too many iterations in selectGlyphs()");
    }

    /**
     * Pythonの __split() 相当
     * 改行(isNewline)を基準に Line オブジェクトの配列に分割する
     */
    _split() {
        const lineLists = Array.from(splitAfter(this.chars, c => c.isNewline));
        return lineLists.map(list => new Line(list));
    }

    /**
     * Pythonの set_position(cntx, char) を完全再現
     */
    setPosition(cntx, char) {
        if (char.prev === null) {
            cntx.x = Math.max(cntx.right - char.left, 0);
            cntx.y = Math.max(cntx.refLine - char.ascent, 0);
        }

        char.setPos(cntx.x, cntx.y);

        if (char.isSpace) {
            try {
                cntx.x = cntx.right + char.dx - (char.next ? char.next.left : 0);
            } catch (e) {
                cntx.x += char.dx;
            }
            try {
                cntx.y = cntx.refLine + char.dy - (char.next ? char.next.ascent : 0);
            } catch (e) {
                cntx.y = cntx.refLine + char.dy;
            }
            cntx.right = cntx.x;
        } 
        else if (char.isNewline) {
            try {
                if (char.next) cntx.right = cntx.margin - char.next.left;
            } catch (e) {}
            cntx.refLine += char.dy;
            cntx.x = cntx.right;
            try {
                cntx.y = cntx.refLine - (char.next ? char.next.ascent : 0);
            } catch (e) {
                cntx.y = cntx.refLine;
            }
        } 
        else if (char.isMarker) {
            try {
                if (char.prev) {
                    char.setPos(char.prev.x, char.prev.y);
                }
            } catch (e) {}
        } 
        else {
            const [exitX, exitY] = char.exit;
            cntx.x = exitX;
            cntx.y = exitY;
            cntx.right = Math.max(cntx.right, char.x + char.right);
        }
    }

    correctLeftAndTop(lines, margin = 5) {
        for (const line of lines) {
            const leftMin = Math.min(...line.chars.map(char => char.x + char.left));
            const xoffset = leftMin < 0 ? (margin - leftMin) : 0;
            for (const char of line.chars) {
                char.setPos(char.x + xoffset, char.y);
            }
        }

        const topMin = Math.min(...this.chars.map(char => char.y + char.top));
        const yoffset = topMin < 0 ? (margin - topMin) : 0;
        for (const char of this.chars) {
            char.setPos(char.x, char.y + yoffset);
        }
    }

    correctInterLine(lines, margin = 5) {
        for (const [upperLine, lowerLine] of pairwise(lines)) {
            const bottom = Math.max(...upperLine.chars.map(char => char.y + char.bottom), 0);
            const top = Math.min(...lowerLine.chars.map(char => char.y + char.top), bottom);
            if (bottom <= top) {
                continue;
            }
            const yoffset = bottom - top + margin;
            for (const char of lowerLine.chars) {
                char.setPos(char.x, char.y + yoffset);
            }
        }
    }

    correctInterClause(lines, margin = 0) {
        for (const line of lines) {
            for (const [leftClause, rightClause] of pairwise(line.clauses)) {
                const leftClauseRight = Math.max(...leftClause.map(char => char.x + char.right), 0);
                const rightClauseLeft = Math.min(...rightClause.map(char => char.x + char.left), leftClauseRight);
                if (leftClauseRight <= rightClauseLeft) {
                    continue;
                }
                const xoffset = leftClauseRight - rightClauseLeft + margin;
                for (const char of rightClause) {
                    char.setPos(char.x + xoffset, char.y);
                }
            }
        }
    }

    /**
     * Pythonの layout() を完全再現
     */
    layout(right = 5, refLine = 20, margin = 5) {
        if (this.chars.length === 0) {
            return new Bbox(0, 0, 0, 0);
        }

        const cntx = new Context({ refLine: refLine, right: right, margin: margin });

        for (const char of this.chars) {
            this.setPosition(cntx, char);
        }

        const lines = this._split();
        this.correctInterLine(lines, margin);
        this.correctInterClause(lines, margin);
        this.correctLeftAndTop(lines, margin);

        const left = Math.floor(Math.min(...this.chars.map(char => char.x + char.left))) - margin;
        const rightVal = Math.ceil(Math.max(...this.chars.map(char => char.x + char.right))) + margin;
        const top = Math.floor(Math.min(...this.chars.map(char => char.y + char.top))) - margin;
        const bottom = Math.ceil(Math.max(...this.chars.map(char => char.y + char.bottom))) + margin;

        return new Bbox(left, rightVal, top, bottom);
    }
    /**
     * Pythonの create_svg を100%再現
     * @return {[string, number]} [SVG文字列, 総再生時間(秒)]
     */
    createSvg({ toAnimate = false, speedMmPerS = 20, toGenerateKeyframe = false, targetS = 0 } = {}) {
        const markerBuf = [];
        const charBuf = [];
        
        // 描画順（マーカーを空白や文字の後ろに回す処理）のシミュレート
        for (const char of this.chars) {
            if (char.isMarker) {
                markerBuf.push(char);
            } else if (char.isSpace || char.isNewline) {
                charBuf.push(char);
                charBuf.push(...markerBuf);
                markerBuf.length = 0; // クリア
            } else {
                charBuf.push(char);
            }
        }
        charBuf.push(...markerBuf);

        const paths = [];
        let timeS = 0;
        
        // 各文字のアニメーション要素をタイムラインに沿って生成
        for (const char of charBuf) {
            const [elem, nextTimeS] = char.createPathElement({
                timeS: timeS,
                toAnimate: toAnimate,
                speedMmPerS: speedMmPerS,
                toGenerateKeyframe: toGenerateKeyframe,
                targetS: targetS
            });
            paths.push(elem);
            timeS = nextTimeS;
        }

        const svgContent = this.svgTemplate(this.bbox).replace('{paths}', paths.join(''));
        return [svgContent, timeS];
    }

    /**
     * Pythonの create_key_frames を再現（スライダー等でのシークや動画書き出し用）
     */
    createKeyFrames(speedMmPerS = 20, framerate = 24) {
        // 全パスの総延長を計算
        const totalLength = this.chars.reduce((sum, c) => sum + c.lengths.reduce((lSum, l) => lSum + l, 0), 0);
        const totalTimeS = totalLength / speedMmPerS;
        const totalFrames = Math.ceil(framerate * totalTimeS);
        
        const frames = [];
        for (let frameNum = 0; frameNum < totalFrames + 4; frameNum++) {
            const targetS = (frameNum * totalTimeS) / totalFrames;
            const [svg] = this.createSvg({
                toAnimate: false,
                speedMmPerS: speedMmPerS,
                toGenerateKeyframe: true,
                targetS: targetS
            });
            frames.push(svg);
        }
        return frames;
    }

    toString() {
        return this.createSvg()[0];
    }
}


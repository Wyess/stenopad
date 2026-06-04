import { ShorthandCharacter } from './Character.js';

export class ShorthandString {
    constructor(rawInput, wordDictionary, stenoDefinitions) {
        this.rawInput = rawInput;
        this.wordDictionary = wordDictionary;
        this.stenoDefinitions = stenoDefinitions;
        this.allCharacters = [];

        this._parseAndConnect();
    }

    _parseAndConnect() {
        // --- 前回実装した最長一致切り出しロジック ---
        const sortedWordKeys = Array.from(this.wordDictionary.keys()).sort((a, b) => b.length - a.length);
        let index = 0;
        const matchedCharNames = [];

        while (index < this.rawInput.length) {
            let matchFound = false;
            const remainingStr = this.rawInput.slice(index);

            for (const wordKey of sortedWordKeys) {
                if (remainingStr.startsWith(wordKey)) {
                    const targetValue = this.wordDictionary.get(wordKey);
                    if (Array.isArray(targetValue)) {
                        matchedCharNames.push(...targetValue);
                    } else {
                        matchedCharNames.push(targetValue);
                    }
                    index += wordKey.length;
                    matchFound = true;
                    break;
                }
            }
            if (!matchFound) {
                matchedCharNames.push(this.rawInput[index]);
                index += 1;
            }
        }

        this.allCharacters = matchedCharNames.map(charName => {
            const def = this.stenoDefinitions.get(charName);
            const tags = def && def.tag ? Object.keys(def.tag) : [];
            const isMarker = tags.includes('marker') || (def && def.marker === true);

            const charObj = new ShorthandCharacter({ name: charName, isMarker, tags });
            // ★追加: 生成時にグリフ定義（仮）を解決させておく
            if (def) {
                charObj.resolveGlyph(def);
            }
            return charObj;
        });

        // 双方向リンク
        const normalChars = this.allCharacters.filter(char => !char.isMarker);
        for (let i = 0; i < normalChars.length; i++) {
            const current = normalChars[i];
            if (i > 0) current.prev = normalChars[i - 1];
            if (i < normalChars.length - 1) current.next = normalChars[i + 1];
        }
    }

        /**
     * 解決されたグリフのパスデータを繋ぎ合わせて本物のSVGを生成する
     * @returns {string} SVGのHTMLソース
     */
    generateSVG() {
        let combinedPaths = '';
        let currentX = 50;  // 描画開始の初期基準 X 座標
        let currentY = 100; // 描画開始の初期基準 Y 座標

        // 拡大率
        const scale = 15;

        this.allCharacters.forEach(char => {
            // グリフが解決されている場合のみ処理に入る
            if (char.selectedGlyph) {

                // 1. パスデータ（線）が存在する場合のみ描画コードを生成
                if (char.selectedGlyph.path && char.selectedGlyph.path.length > 0) {
                    char.selectedGlyph.path.forEach(pathSeg => {
                        if (pathSeg.d) {
                            combinedPaths += `
                                <g transform="translate(${currentX}, ${currentY}) scale(${scale})">
                                    <path d="${pathSeg.d}" fill="none" stroke="#333333" stroke-width="0.2" stroke-linecap="round" stroke-linejoin="round" />
                                </g>
                            `;
                        }
                    });
                }

                // 2. パスの有無に関わらず、dx, dy が定義されていれば必ず座標を加算する（位置調整用）
                const dx = char.selectedGlyph.dx || 0;
                const dy = char.selectedGlyph.dy || 0;

                currentX += dx * scale;
                currentY += dy * scale;
            }
        });

        // 画面幅いっぱいに広がるSVGコンテナで包んで出力
        return `
            <svg width="100%" height="300" viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg" style="border: 1px dashed #ccc; background: #fff;">
                <line x1="0" y1="100" x2="1000" y2="100" stroke="#eee" stroke-width="1" />
                ${combinedPaths}
            </svg>
        `;
    }
}


export class ShorthandCharacter {
    constructor({ name, isMarker = false, tags = [] }) {
        this.name = name;        // "A" や "Kyou" などの内部文字名
        this.isMarker = isMarker;
        this.tags = tags || [];
        this.prev = null;
        this.next = null;
        
        // 確定したグリフ情報を保持するプロパティ
        this.selectedGlyph = null;
    }

    /**
     * 前後の隣接情報を辿る（互換性のために残すメソッド）
     */
    getNeighbor(offset) {
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

    /**
     * 【フェーズ1】文脈評価をスキップし、デフォルトのグリフを確定させる
     * @param {Object} rawDef - stenoDefinitions から取得したこの文字の生の定義オブジェクト
     */
    resolveGlyph(rawDef) {
        if (!rawDef) return;

        // 1. default_glyph があれば最優先
        if (rawDef.default_glyph) {
            this.selectedGlyph = rawDef.default_glyph;
            return;
        }

        // 2. なければ glyphs 配列の先頭要素を選択
        if (rawDef.glyphs && rawDef.glyphs.length > 0) {
            this.selectedGlyph = rawDef.glyphs[0];
            return;
        }
    }
}


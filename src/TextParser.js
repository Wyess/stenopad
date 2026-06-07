export class TextParser {
    /**
     * @param {Object} wdict - 辞書データ (sh['dictionary'])
     * @param {Object} trie - Trie木データ (sh['trie'])
     */
    constructor(wdict, trie) {
        this.dict = wdict || {};
        this.trie = trie || {};
        
        // デフォルト値の設定 (Python側の挙動を再現)
        if (!this.dict['\n']) {
            this.dict['\n'] = ['Newline'];
        }
        this.sep = this.dict['SEPARATOR'] || '\x1F';
    }

    ensureList(arg) {
        if (Array.isArray(arg)) return arg;
        return [arg];
    }

    /**
     * Pythonの break_word(string) の最長一致ロジックを再現
     */
    *breakWord(string) {
        const n = string.length;
        let start = 0;
        while (start < n) {
            let node = this.trie;
            let word = string[start];
            
            for (let pos = start; pos < n; pos++) {
                const c = string[pos];
                if (node && c in node) {
                    node = node[c];
                    if (node && node['word']) {
                        word = node['word'];
                    }
                } else {
                    break;
                }
            }
            
            const chars = this.dict[word] || 'Null';
            start += word.length;
            yield* this.ensureList(chars);
        }
    }

    /**
     * 単語（WORD）トークンの処理
     */
    parseWord(tok) {
        if (this.dict[tok]) {
            return this.ensureList(this.dict[tok]);
        }

        if (tok.includes(this.sep)) {
            const words = tok.split(this.sep).filter(Boolean);
            const schars = [];
            for (const word of words) {
                schars.push(...this.parseWord(word));
            }
            return schars;
        }

        return Array.from(this.breakWord(tok));
    }

    /**
     * 空白（WHITESPACE）トークンの処理
     */
    parseWhitespace(tok) {
        return this.ensureList(this.dict[tok] || ['Space']);
    }

    /**
     * Python版 InputTextTransformer.text(args) のバッファ制御を再現
     * 連続する空白・改行が次の通常単語の前に正しくマージされるように処理します
     */
    parse(text) {
        // Larkパーサーの代わりに、正規表現で「非空白の連続（WORD）」と「空白の連続（WHITESPACE）」に分解
        const tokens = text.match(/\s+|\S+/g) || [];
        
        const args = tokens.map(tok => {
            if (/\s/.test(tok)) {
                return this.parseWhitespace(tok);
            } else {
                return this.parseWord(tok);
            }
        });

        const ret = [];
        let buf = [];

        for (const arg of args) {
            if (arg.length > 0 && (arg[0] === 'Space' || arg[0] === 'Newline')) {
                buf.push(...arg);
            } else {
                ret.push(...buf);
                ret.push(...arg);
                buf = [];
            }
        }
        // 末尾に残った空白バッファはPython版の仕様通り捨てる（または必要に応じて結合）
        return ret;
    }
}

/**
 * 外部から簡単に呼び出すためのラップ関数
 */
export function parseText(text, wdict, trie) {
    const parser = new TextParser(wdict, trie);
    return parser.parse(text);
}


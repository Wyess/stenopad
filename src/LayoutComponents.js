// Pythonの split_after(iterable, pred) を再現
export function* splitAfter(iterable, pred) {
    let buf = [];
    for (const item of iterable) {
        buf.push(item);
        if (pred(item)) {
            yield buf;
            buf = [];
        }
    }
    if (buf.length > 0) {
        yield buf;
    }
}

// Pythonの pairwise(iterable) を再現
export function* pairwise(iterable) {
    const iterator = iterable[Symbol.iterator]();
    let a = iterator.next();
    if (a.done) return;

    let current = a.value;
    let next = iterator.next();
    while (!next.done) {
        yield [current, next.value];
        current = next.value;
        next = iterator.next();
    }
}

export class Context {
    constructor({ x = 0, y = 0, refLine = 0, right = 0, margin = 5 } = {}) {
        this.x = x;
        this.y = y;
        this.refLine = refLine;
        this.right = right;
        this.margin = margin;
    }
}

export class Line {
    constructor(chars = []) {
        this.chars = chars;
    }

    // Pythonの @property def clauses(self): を再現
    get clauses() {
        return Array.from(splitAfter(this.chars, c => c.isSpace));
    }
}

export class Bbox {
    constructor(left, right, top, bottom) {
        this.left = left;
        this.right = right;
        this.top = top;
        this.bottom = bottom;
        this.width = right - left;
        this.height = bottom - top;
    }

    // Pythonの __mul__ (スケール倍演算) を再現
    multiply(scale) {
        return new Bbox(
            this.left * scale,
            this.right * scale,
            this.top * scale,
            this.bottom * scale
        );
    }

    // SVGの viewBox 属性用文字列への変換 (Pythonの __str__ 相当)
    toString() {
        return `${this.left} ${this.top} ${this.width} ${this.height}`;
    }
}


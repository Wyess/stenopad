/**
 * 1. 静的SVGのダウンロード
 */
export function downloadSvg(shorthandStringInstance, fileName = "shorthand.svg") {
    // 通常の静的描画SVGを取得
    const svgText = shorthandStringInstance.createSvg({ toAnimate: false })[0];
    
    const blob = new Blob([svgText], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();
    
    URL.revokeObjectURL(url);
}

/**
 * 2. アニメーションSVG (SMIL) のダウンロード
 */
export function downloadAnimatedSvg(shorthandStringInstance, fileName = "shorthand_animated.svg") {
    // `<animate>` 要素を含んだ動的SVGを取得
    const svgText = shorthandStringInstance.createSvg({ toAnimate: true })[0];
    
    const blob = new Blob([svgText], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();
    
    URL.revokeObjectURL(url);
}
export function downloadPng(shorthandStringInstance, fileName = "shorthand.png") {
    let svgText = shorthandStringInstance.createSvg({ toAnimate: false })[0];
    const bbox = shorthandStringInstance.bbox;
    
    svgText = svgText
        .replace(`width="${bbox.width}mm"`, `width="${bbox.width}"`)
        .replace(`height="${bbox.height}mm"`, `height="${bbox.height}"`);

    const svgBlob = new Blob([svgText], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);
    
    const img = new Image();
    img.onload = () => {
        // 💡 1. 解像度の倍率を大幅に引き上げる (12倍〜16倍など)
        // もしこれでも足りない場合は 16 や 20 にしてみてください
        const scale = 12; 
        
        const canvas = document.createElement("canvas");
        // Canvas自体の物理的なピクセルサイズを巨大にする
        canvas.width = bbox.width * scale;
        canvas.height = bbox.height * scale;
        
        const ctx = canvas.getContext("2d");
        
        // 背景を白で塗りつぶす
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 💡 2. 画像のアンチエイリアス（平滑化）を有効にして線を滑らかにする
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = "high";
        
        // 💡 3. 元画像全体(0,0〜width,height)を、
        // Canvas全体(0,0〜巨大化したwidth,height)へジャストマッピングする
        ctx.drawImage(
            img,
            0, 0, bbox.width, bbox.height,       // sx, sy, sw, sh (元画像の全領域)
            0, 0, canvas.width, canvas.height    // dx, dy, dw, dh (Canvasの全領域に引き伸ばし)
        );
        
        // PNGとして書き出し
        const pngUrl = canvas.toDataURL("image/png");
        const a = document.createElement("a");
        a.href = pngUrl;
        a.download = fileName;
        a.click();
        
        URL.revokeObjectURL(url);
    };
    
    img.src = url;
}


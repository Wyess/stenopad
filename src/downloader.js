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

/**
 * GIFアニメーションのダウンロード (サムネイルでも絶対に動く・完全修正版)
 */
export function downloadShorthandGif(shorthandStringInstance) {
    const fps = 20;
    const svgFrames = shorthandStringInstance.createKeyFrames(15, fps);
    const bbox = shorthandStringInstance.bbox;

    // 💡 解像度を上げるための倍率（4倍〜6倍程度が、GIFのファイルサイズとクッキリ感のベストバランスです）
    const scale = 6;
    const scaledWidth = bbox.width * scale;
    const scaledHeight = bbox.height * scale;

    // 1. 各フレームを高解像度で確実にレンダリング
    const promises = svgFrames.map(svgText => {
        return new Promise((resolve) => {
            // mm単位を排除してピクセルとしてブラウザに認識させる
            const fixedSvg = svgText
                .replace(`width="${bbox.width}mm"`, `width="${bbox.width}"`)
                .replace(`height="${bbox.height}mm"`, `height="${bbox.height}"`);

            const blob = new Blob([fixedSvg], { type: "image/svg+xml;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const img = new Image();

            img.onload = () => {
                const canvas = document.createElement("canvas");
                // 💡 Canvasの物理的なピクセル数を巨大化
                canvas.width = scaledWidth;
                canvas.height = scaledHeight;

                const ctx = canvas.getContext("2d");

                // 背景を白で塗りつぶす
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // アンチエイリアスを最大に
                ctx.imageSmoothingEnabled = true;
                ctx.imageSmoothingQuality = "high";

                // 💡 ここがポイント：描画座標全体をスケールアップしてからSVGを描画する
                ctx.drawImage(
                    img,
                    0, 0, bbox.width, bbox.height,       // 元画像の全領域
                    0, 0, canvas.width, canvas.height    // Canvasの全領域（巨大）へジャストフィット
                );

                // 高解像度なPNGデータとして書き出し
                const dataUrl = canvas.toDataURL("image/png");
                URL.revokeObjectURL(url);
                resolve(dataUrl);
            };
            img.src = url;
        });
    });

    // 2. 高解像度化されたフレーム群を、適切なサイズでGIFにバインド
    Promise.all(promises).then((images) => {
        gifshot.createGIF({
            images: images,
            // 💡 ここを scaledWidth/Height にすることで、
            // 5倍密度のクッキリした画像がそのまま高解像度GIF（Retina対応）として出力されます
            gifWidth: scaledWidth,
            gifHeight: scaledHeight,
            interval: 1 / fps,
            numFrames: images.length,
            loop: 0
        }, function(obj) {
            if (!obj.error) {
                const a = document.createElement("a");
                a.href = obj.image;
                a.download = "shorthand_animation.gif";
                a.click();
            } else {
                console.error("GIF生成エラー:", obj.error);
            }
        });
    });
}
/**
 * MediaRecorderを使用した動画(WebM)のダウンロード (進捗コールバック付き)
 */
export function downloadShorthandVideo(shorthandStringInstance, onProgress, onComplete, fileName = "shorthand_animation.webm") {
    const fps = 24;
    const svgFrames = shorthandStringInstance.createKeyFrames(20, fps);
    const bbox = shorthandStringInstance.bbox;

    const scale = 5;
    const canvas = document.createElement("canvas");
    canvas.width = bbox.width * scale;
    canvas.height = bbox.height * scale;
    const ctx = canvas.getContext("2d");

    const stream = canvas.captureStream(fps);
    let options = { mimeType: 'video/webm; codecs=vp9' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) options = { mimeType: 'video/webm; codecs=vp8' };

    const recorder = new MediaRecorder(stream, options);
    const chunks = [];

    recorder.ondataavailable = (e) => { if (e.data && e.data.size > 0) chunks.push(e.data); };

    recorder.onstop = () => {
        const videoBlob = new Blob(chunks, { type: options.mimeType });
        const videoUrl = URL.createObjectURL(videoBlob);

        const a = document.createElement("a");
        a.href = videoUrl;
        a.download = fileName;
        a.click();

        URL.revokeObjectURL(videoUrl);
        if (onComplete) onComplete(); // 💡 完了コールバック
    };

    recorder.start();

    let currentFrame = 0;
    const totalFrames = svgFrames.length;

    function renderNextFrame() {
        if (currentFrame >= totalFrames) {
            // 最後の進捗100%を通知
            if (onProgress) onProgress(100);
            setTimeout(() => { recorder.stop(); }, 500);
            return;
        }

        // 💡 現在の進捗率（％）を計算してコールバックに送る
        if (onProgress && totalFrames > 0) {
            const percent = Math.floor((currentFrame / totalFrames) * 100);
            onProgress(percent);
        }

        const svgText = svgFrames[currentFrame];
        const fixedSvg = svgText
            .replace(`width="${bbox.width}mm"`, `width="${bbox.width}"`)
            .replace(`height="${bbox.height}mm"`, `height="${bbox.height}"`);

        const blob = new Blob([fixedSvg], { type: "image/svg+xml;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const img = new Image();

        img.onload = () => {
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(img, 0, 0, bbox.width, bbox.height, 0, 0, canvas.width, canvas.height);

            URL.revokeObjectURL(url);
            currentFrame++;
            setTimeout(renderNextFrame, 1000 / fps);
        };
        img.src = url;
    }

    renderNextFrame();
}


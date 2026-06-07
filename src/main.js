import { ShorthandString } from './ShorthandString.js';
import { downloadSvg, downloadAnimatedSvg, downloadPng } from './downloader.js';

const stenoInput = document.getElementById('steno-input');
const stenoSvgOutput = document.getElementById('steno-svg-output');
const appContainer = document.querySelector('.app-container');

let wasedaData;

// 速記定義を保持する Map
let stenoDefinitions = new Map();
let wordDictionary = new Map();   // dictionary の内容を保持


function adjustHeight() {
    if (window.visualViewport) {
        appContainer.style.height = `${window.visualViewport.height}px`;
    } else {
        appContainer.style.height = `${window.innerHeight}px`;
    }
}

/**
 * 起動時に一度だけ実行されるJSONデータの読み込み処理
 */
async function loadAssets() {
    try {
        stenoSvgOutput.innerHTML = `<p style="color: #666; text-align: center; margin-top: 40px;">定義データを読み込み中...</p>`;
        
        const response = await fetch('./src/waseda.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        //const wasedaData = await response.json();
        wasedaData = await response.json();

        const waseda = wasedaData.waseda || {};

        // 1. 単語辞書 (dictionary) の展開
        if (waseda.dictionary) {
            Object.entries(waseda.dictionary).forEach(([word, target]) => {
                wordDictionary.set(word, target);
            });
        }

        // 2. 速記文字定義 (character) の展開
        if (waseda.character) {
            Object.entries(waseda.character).forEach(([charName, data]) => {
                stenoDefinitions.set(charName, data);
            });
        }

        console.log(`データの読み込みが完了しました。 (単語辞書: ${wordDictionary.size}件, 文字定義: ${stenoDefinitions.size}件)`);
        stenoSvgOutput.innerHTML = `<p style="color: #999; text-align: center; margin-top: 40px;">準備完了。ここに入力された速記文字が表示されます。</p>`;
        
        stenoInput.disabled = false;
        stenoInput.focus();

    } catch (error) {
        console.error("アセットの読み込みに失敗しました:", error);
        stenoSvgOutput.innerHTML = `<p style="color: #dc3545; text-align: center; margin-top: 40px;">データの読み込みに失敗しました: ${error.message}</p>`;
    }
}

async function init() {
    console.log("Stenopad JS ランタイムが起動しました。");
    stenoInput.disabled = true;

    adjustHeight();
    if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', adjustHeight);
    } else {
        window.addEventListener('resize', adjustHeight);
    }

    await loadAssets();
    stenoInput.addEventListener('input', handleInputChange);
}

/**
 * テキスト入力が発生するたびに呼び出されるハンドラー
 */
function handleInputChange(event) {
    const text = event.target.value;

    if (text.length === 0) {
        stenoSvgOutput.innerHTML = `<p style="color: #999; text-align: center; margin-top: 40px;">ここに速記文字（SVG）が表示されます</p>`;
        return;
    }

    // ロジックの実行
    //const stenoString = new ShorthandString(text, wordDictionary, stenoDefinitions);
    const stenoString = new ShorthandString(text, wasedaData.waseda);

    // ★ 暫定の青丸デバッグを、本物のSVG描画に差し替え！
    //stenoSvgOutput.innerHTML = stenoString.toString();
    stenoSvgOutput.innerHTML = stenoString.createSvg({toAnimate: false})[0];
}

/**
 * 分割された Character の配列を受け取ってダミーSVGを生成する
 * @param {Array<ShorthandCharacter>} characters 
 */
function createDebugSVG(characters) {
    const tokenCount = characters.length;
    const svgHeight = Math.max(Math.ceil(tokenCount / 10) * 80, 120);
    
    let contents = '';
    for (let i = 0; i < tokenCount; i++) {
        const charObj = characters[i];
        
        // 1区画の座標計算
        const cx = (i % 10) * 75 + 45;
        const cy = Math.floor(i / 10) * 80 + 40;

        // マーカー文字は オレンジ、通常文字は 青 で色分けしてリンクの除外状態を目視確認
        const badgeColor = charObj.isMarker ? '#ff9800' : '#007bff';

        contents += `
            <g>
                <circle cx="${cx}" cy="${cy}" r="30" fill="${badgeColor}" opacity="0.9" />
                <text x="${cx}" y="${cy + 5}" fill="white" font-size="12" font-weight="bold" text-anchor="middle">${charObj.name}</text>
                <text x="${cx}" y="${cy + 22}" fill="white" font-size="8" text-anchor="middle">${charObj.isMarker ? 'Marker' : 'Normal'}</text>
            </g>
        `;
    }
    return `<svg width="100%" height="${svgHeight}" viewBox="0 0 800 ${svgHeight}" xmlns="http://www.w3.org/2000/svg" style="border: 1px dashed #bbb; background: #fafafa;">${contents}</svg>`;
}

window.addEventListener('DOMContentLoaded', init);

let currentShorthand = null; 

// 例: テキスト入力時に描画・保持
document.getElementById("steno-input").addEventListener("input", (e) => {
    currentShorthand = new ShorthandString(e.target.value, wasedaData.waseda);
    document.getElementById("steno-svg-output").innerHTML = currentShorthand.toString();
});

// 各ボタンのイベントバインディング
document.getElementById("btn_svg").addEventListener("click", () => {
    if (currentShorthand) downloadSvg(currentShorthand);
});
document.getElementById("btn_anisvg").addEventListener("click", () => {
    if (currentShorthand) downloadAnimatedSvg(currentShorthand);
});
document.getElementById("btn_png").addEventListener("click", () => {
    if (currentShorthand) downloadPng(currentShorthand);
});

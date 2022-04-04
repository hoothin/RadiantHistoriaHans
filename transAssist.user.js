// ==UserScript==
// @name         光辉物语翻译辅助
// @namespace    hoothin
// @version      0.2.3
// @description  为光辉物语汉化项目在腾讯文档顶部添加翻译辅助按钮，点击条目后增加翻译直达按钮
// @author       hoothin
// @include      https://docs.qq.com/sheet/DWnZ6a2hpUkJRd2JZ*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        GM_setClipboard
// @license      MIT License
// ==/UserScript==

(function() {
    'use strict';
    const wordPlace = [
        ["Vainqueur","ヴァンクール","梵奎尔"],
        ["Cygnus","シグナス","希格纳斯"],
        ["Alistel","アリステル","阿里斯特尔"],
        ["Granorg","グランオルグ","格兰奥冈"],
        ["Imperial Ruins","帝国跡地","帝国遗迹"],
        ["Audience Hall","謁見の間","谒见之间"],
        ["Palace","王宮","王宫"],
        ["El Dorado","エルドラド","埃尔多拉多"],
        ["Cornet Village","コルネ村","科恩村"],
        ["Alma Mine","アルマ鉱山","阿尔玛矿厂"],
        ["downtown","観光区","观光区"],
        ["Gran Plain","グラン平原","格兰平原"],
        ["lodging","宿屋","旅馆"],
        ["Forest Square","森の広場","森之广场"],
        ["South Hill","南の高台","南之高台"],
        ["south hill","南の丘","南之丘"]
    ];
    const wordName = [
        ["Marco","マルコ","马尔可"],
        ["Eruca","エルーカ","艾露卡"],
        ["Selvan","セルバン","塞尔凡"],
        ["Stocke","ストック","斯托克"],
        ["Dias","ディアス","迪亚斯"],
        ["Queen","Eruca","艾露卡女王"],
        ["Sir Dias","ディアス様","迪亚斯爵士"],
        ["Protea","プロテア","普罗蒂亚"],
        ["Resistance","レジスタンス","抵抗军"],
        ["Queen","Protea","普罗蒂亚女王"],
        ["Will","ウィル","威尔"],
        ["Princess Eruca","","艾露卡王女"],
        ["Lady Eruca","","艾露卡大人"],
        ["Count Selvan","セルバン伯爵","塞尔凡伯爵"],
        ["Prophet Noah","ノア様","诺亚先知"],
        ["Liese","","莉丝"],
        ["Rosch","","罗施"],
        ["Field Marshal Viola","ビオラ准将","薇奥拉准将"],
        ["Aht","","阿托"],
        ["Granorg army","グランオルグ騎士団","格兰奥冈骑士团"],
        ["Hugo","","雨果"],
        ["Noah guy","","诺亚大人"],
        ["Fennel","フェンネル","芬内鲁"],
        ["Bram","ブラム","布拉姆"],
        ["Sir Dias","騎士団長ディアス","骑士团长迪亚斯"],
        ["Garland","ガーランド","加兰德"]
    ];
    const wordItem = [
        ["Divine Water","神聖水","圣水"],
        ["Death Crimson","デスクリムゾン","死亡猩红"],
        ["Sand Sword","砂の剣","沙剑"],
        ["Anti−Curse","アンチカース","反诅咒"],
        ["Red Knife","レッドナイフ","红刀"],
        ["Tourniquets","救命薬","救命药"],
        ["thaumatech","魔動機械","魔动机械"],
        ["Element Shell","エレメントシェル","元素外壳"],
        ["Celes Branch","セレスのえだ","赛雷斯之枝"],
        ["Thaumachine","魔動兵","魔动兵"]
    ];
    const wordOther = [
        ["White Chronicle","白示録","白示录"],
        ["Strike","スマッシュ","打击"],
        ["swordsman","剣士","剑士"],
        ["possible world","可能性世界","可能性世界"],
        ["node","刻印","刻印"],
        ["Alistellians","","阿里斯特尔人"]
    ];
    var transBody = "";
    var tagCon,btnOrder;
    function initListener() {
        var formulaInput = document.querySelector("div.formula-input");
        var barLabel = document.querySelector("div.bar-label");
        document.querySelector("div.excel-container").addEventListener("click", e => {
            if(/^C/.test(barLabel.innerText))return;
            transBody = dbC2sbC(formulaInput.innerText.split("\n")[0].replace(/\<p\>/g,"\n").replace(/\<.*?\>/g," ")).trim();
            if(transBody){
                btnOrder.style.display = "";
                tagCon.innerHTML = "";
                checkWord(wordPlace, transBody);
                checkWord(wordName, transBody);
                checkWord(wordItem, transBody);
                checkWord(wordOther, transBody);
            }
        });
    }

    function initView() {
        btnOrder = document.createElement("div");
        btnOrder.style.cssText = "position: fixed;top: 10px;width: 100%;z-index: 9;text-align: center;pointer-events: none;display: none";

        var transSpan = document.createElement("span");
        var gooBtn = createTransBtn("Google", (target) => {
            window.open(`https://translate.google.cn/?client=gtx&dj=1&q=${target}&sl=auto&tl=zh-CN&hl=zh-CN&ie=UTF-8&oe=UTF-8&source=icon&dt=t&dt=bd`,'_blank','height=600,width=800,left=30,top=30,location=no,status=no,toolbar=no,menubar=no,scrollbars=yes');
        });
        var bdBtn = createTransBtn("Baidu", (target) => {
            window.open(`https://fanyi.baidu.com/#auto/zh/${target}`,'_blank','height=600,width=1200,left=30,top=30,location=no,status=no,toolbar=no,menubar=no,scrollbars=yes');
        });
        var deeplBtn = createTransBtn("Deepl", (target) => {
            window.open(`https://www.deepl.com/zh/translator#auto/zh/${target}`,'_blank','height=600,width=800,left=30,top=30,location=no,status=no,toolbar=no,menubar=no,scrollbars=yes');
        });
        var papagoBtn = createTransBtn("Papago", (target) => {
            window.open(`https://papago.naver.com/?sk=auto&tk=zh-CN&st=${target}`,'_blank','height=600,width=800,left=30,top=30,location=no,status=no,toolbar=no,menubar=no,scrollbars=yes');
        });
        transSpan.style.cssText = "padding-right: 5px;pointer-events: all;";
        transSpan.appendChild(gooBtn);
        transSpan.appendChild(bdBtn);
        transSpan.appendChild(deeplBtn);
        transSpan.appendChild(papagoBtn);
        btnOrder.appendChild(transSpan);

        tagCon = document.createElement("span");
        tagCon.style.pointerEvents="all";
        btnOrder.appendChild(tagCon);

        document.body.appendChild(btnOrder);
    }

    function createTransBtn(serverName, clickFun) {
        var transBtn = document.createElement("button");
        transBtn.style.cssText = "padding: 3px;cursor: pointer;"
        transBtn.innerText = serverName;
        transBtn.addEventListener("click", e=>{
            if(transBody){
                clickFun(encodeURIComponent(transBody));
            }
        });
        return transBtn;
    }

    function checkWord(dictArr, str) {
        dictArr.forEach(target => {
            if(target.length != 3)return;
            if((target[0] && new RegExp("\\b"+target[0]+"\\b","i").test(str)) || (target[1] && str.indexOf(target[1]) != -1)){
                createTag(target[2]);
            }
        });
    }

    function createTag(str){
        var tagBtn = document.createElement("button");
        tagBtn.style.cssText = "padding: 3px;cursor: pointer;";
        tagBtn.innerText = str;
        tagBtn.title = "点击复制";
        tagBtn.addEventListener("click", e => {
            GM_setClipboard(str);
            tagBtn.innerText = "复制成功";
            setTimeout(()=>{if(tagBtn && tagBtn.parentNode)tagBtn.innerText = str;}, 500);
        });
        tagCon.appendChild(tagBtn);
    }

    function dbC2sbC(str){
        var result="",d;
        for(var i=0;i<str.length;i++) {
            var code = str.charCodeAt(i);
            if (code >= 65281 && code <= 65373) {
                d=str.charCodeAt(i)-65248;
                result += String.fromCharCode(d);
            } else if (code == 12288) {
                d=str.charCodeAt(i)-12288+32;
                result += String.fromCharCode(d);
            } else {
                result += str.charAt(i);
            }
        }
        return result;
    }

    function init() {
        initView();
        initListener();
    }

    init();
})();
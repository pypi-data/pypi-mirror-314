/*! For license information please see async-feffery_shortcut_panel.js.LICENSE.txt */
(window.webpackJsonpfeffery_utils_components=window.webpackJsonpfeffery_utils_components||[]).push([[30],{541:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var react__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),react__WEBPACK_IMPORTED_MODULE_0___default=__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__),_components_other_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(244),ninja_keys__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(977),lodash__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(26),lodash__WEBPACK_IMPORTED_MODULE_3___default=__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_3__),_components_styleControl_FefferyStyle_react__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(98);function _typeof(t){return(_typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function ownKeys(t,e){var i=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),i.push.apply(i,n)}return i}function _objectSpread(t){for(var e=1;e<arguments.length;e++){var i=null!=arguments[e]?arguments[e]:{};e%2?ownKeys(Object(i),!0).forEach((function(e){_defineProperty(t,e,i[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(i)):ownKeys(Object(i)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(i,e))}))}return t}function _defineProperty(t,e,i){return(e=_toPropertyKey(e))in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}function _toPropertyKey(t){var e=_toPrimitive(t,"string");return"symbol"==_typeof(e)?e:e+""}function _toPrimitive(t,e){if("object"!=_typeof(t)||!t)return t;var i=t[Symbol.toPrimitive];if(void 0!==i){var n=i.call(t,e||"default");if("object"!=_typeof(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}var footerHtmlEn=react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div",{class:"modal-footer",slot:"footer"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{class:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"enter"),"to select"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"})),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"})),"to navigate"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"esc"),"to close"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"backspace"),"move to parent")),footerHtmlZh=react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div",{className:"modal-footer",slot:"footer"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"enter"),"选择"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"})),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"})),"上下切换"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"esc"),"关闭面板"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"backspace"),"回到上一级")),locale2footer=new Map([["en",footerHtmlEn],["zh",footerHtmlZh]]),locale2placeholder=new Map([["en","Type a command or search..."],["zh","输入指令或进行搜索..."]]),FefferyShortcutPanel=function FefferyShortcutPanel(props){var id=props.id,data=props.data,placeholder=props.placeholder,openHotkey=props.openHotkey,theme=props.theme,locale=props.locale,open=props.open,close=props.close,panelStyles=props.panelStyles,setProps=props.setProps,loading_state=props.loading_state;data=data.map((function(t){return Object(lodash__WEBPACK_IMPORTED_MODULE_3__.isString)(t.handler)||t.hasOwnProperty("children")?t:_objectSpread(_objectSpread({},t),{handler:function(){setProps({triggeredHotkey:{id:t.id,timestamp:Date.parse(new Date)}})}})}));var ninjaKeys=Object(react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);return Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)((function(){ninjaKeys.current&&ninjaKeys.current.addEventListener("change",(function(t){setProps({searchValue:t.detail.search})}))}),[]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)((function(){ninjaKeys.current&&(ninjaKeys.current.data=data.map((function(item){return Object(lodash__WEBPACK_IMPORTED_MODULE_3__.isString)(item.handler)?_objectSpread(_objectSpread({},item),{handler:eval(item.handler)}):item})))}),[data]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)((function(){ninjaKeys.current&&open&&(ninjaKeys.current.open(),setProps({open:!1}))}),[open]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)((function(){ninjaKeys.current&&close&&(ninjaKeys.current.close(),setProps({close:!1}))}),[close]),panelStyles=_objectSpread(_objectSpread({},{width:"640px",overflowBackground:"rgba(255, 255, 255, 0.5)",textColor:"rgb(60, 65, 73)",fontSize:"16px",top:"20%",accentColor:"rgb(110, 94, 210)",secondaryBackgroundColor:"rgb(239, 241, 244)",secondaryTextColor:"rgb(107, 111, 118)",selectedBackground:"rgb(248, 249, 251)",actionsHeight:"300px",groupTextColor:"rgb(144, 149, 157)",zIndex:1}),panelStyles),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react__WEBPACK_IMPORTED_MODULE_0___default.a.Fragment,null,react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_styleControl_FefferyStyle_react__WEBPACK_IMPORTED_MODULE_4__.a,{rawStyle:"\nninja-keys {\n    --ninja-width: ".concat(panelStyles.width,";\n    --ninja-overflow-background: ").concat(panelStyles.overflowBackground,";\n    --ninja-text-color: ").concat(panelStyles.textColor,";\n    --ninja-font-size: ").concat(panelStyles.fontSize,";\n    --ninja-top: ").concat(panelStyles.top,";\n    --ninja-accent-color: ").concat(panelStyles.accentColor,";\n    --ninja-secondary-background-color: ").concat(panelStyles.secondaryBackgroundColor,";\n    --ninja-secondary-text-color: ").concat(panelStyles.secondaryTextColor,";\n    --ninja-selected-background: ").concat(panelStyles.selectedBackground,";\n    --ninja-actions-height: ").concat(panelStyles.actionsHeight,";\n    --ninja-group-text-color: ").concat(panelStyles.groupTextColor,";\n    --ninja-z-index: ").concat(panelStyles.zIndex,";\n}\n")}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("ninja-keys",{id:id,class:theme,ref:ninjaKeys,placeholder:placeholder||locale2placeholder.get(locale),openHotkey:openHotkey,hotKeysJoinedView:!0,hideBreadcrumbs:!0,"data-dash-is-loading":loading_state&&loading_state.is_loading||void 0},locale2footer.get(locale)))};__webpack_exports__.default=FefferyShortcutPanel,FefferyShortcutPanel.defaultProps=_components_other_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__.b,FefferyShortcutPanel.propTypes=_components_other_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__.c},977:function(t,e,i){"use strict";const n=window,s=n.ShadowRoot&&(void 0===n.ShadyCSS||n.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,o=Symbol(),r=new WeakMap;class a{constructor(t,e,i){if(this._$cssResult$=!0,i!==o)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(s&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=r.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&r.set(e,t))}return t}toString(){return this.cssText}}const l=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,n)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[n+1],t[0]);return new a(i,t,o)},c=s?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new a("string"==typeof t?t:t+"",void 0,o))(e)})(t):t;var h;const d=window,p=d.trustedTypes,u=p?p.emptyScript:"",_=d.reactiveElementPolyfillSupport,f={toAttribute(t,e){switch(e){case Boolean:t=t?u:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},v=(t,e)=>e!==t&&(e==e||t==t),y={attribute:!0,type:String,converter:f,reflect:!1,hasChanged:v};class m extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(t){var e;this.finalize(),(null!==(e=this.h)&&void 0!==e?e:this.h=[]).push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach((e,i)=>{const n=this._$Ep(i,e);void 0!==n&&(this._$Ev.set(n,i),t.push(n))}),t}static createProperty(t,e=y){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const i="symbol"==typeof t?Symbol():"__"+t,n=this.getPropertyDescriptor(t,i,e);void 0!==n&&Object.defineProperty(this.prototype,t,n)}}static getPropertyDescriptor(t,e,i){return{get(){return this[e]},set(n){const s=this[t];this[e]=n,this.requestUpdate(t,s,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||y}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),void 0!==t.h&&(this.h=[...t.h]),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,e=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const i of e)this.createProperty(i,t[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(c(t))}else void 0!==t&&e.push(c(t));return e}static _$Ep(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}_$Eu(){var t;this._$E_=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null===(t=this.constructor.h)||void 0===t||t.forEach(t=>t(this))}addController(t){var e,i;(null!==(e=this._$ES)&&void 0!==e?e:this._$ES=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(i=t.hostConnected)||void 0===i||i.call(t))}removeController(t){var e;null===(e=this._$ES)||void 0===e||e.splice(this._$ES.indexOf(t)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((t,e)=>{this.hasOwnProperty(e)&&(this._$Ei.set(e,this[e]),delete this[e])})}createRenderRoot(){var t;const e=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return((t,e)=>{s?t.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet):e.forEach(e=>{const i=document.createElement("style"),s=n.litNonce;void 0!==s&&i.setAttribute("nonce",s),i.textContent=e.cssText,t.appendChild(i)})})(e,this.constructor.elementStyles),e}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostConnected)||void 0===e?void 0:e.call(t)})}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostDisconnected)||void 0===e?void 0:e.call(t)})}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$EO(t,e,i=y){var n;const s=this.constructor._$Ep(t,i);if(void 0!==s&&!0===i.reflect){const o=(void 0!==(null===(n=i.converter)||void 0===n?void 0:n.toAttribute)?i.converter:f).toAttribute(e,i.type);this._$El=t,null==o?this.removeAttribute(s):this.setAttribute(s,o),this._$El=null}}_$AK(t,e){var i;const n=this.constructor,s=n._$Ev.get(t);if(void 0!==s&&this._$El!==s){const t=n.getPropertyOptions(s),o="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==(null===(i=t.converter)||void 0===i?void 0:i.fromAttribute)?t.converter:f;this._$El=s,this[s]=o.fromAttribute(e,t.type),this._$El=null}}requestUpdate(t,e,i){let n=!0;void 0!==t&&(((i=i||this.constructor.getPropertyOptions(t)).hasChanged||v)(this[t],e)?(this._$AL.has(t)||this._$AL.set(t,e),!0===i.reflect&&this._$El!==t&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(t,i))):n=!1),!this.isUpdatePending&&n&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach((t,e)=>this[e]=t),this._$Ei=void 0);let e=!1;const i=this._$AL;try{e=this.shouldUpdate(i),e?(this.willUpdate(i),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostUpdate)||void 0===e?void 0:e.call(t)}),this.update(i)):this._$Ek()}catch(t){throw e=!1,this._$Ek(),t}e&&this._$AE(i)}willUpdate(t){}_$AE(t){var e;null===(e=this._$ES)||void 0===e||e.forEach(t=>{var e;return null===(e=t.hostUpdated)||void 0===e?void 0:e.call(t)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return!0}update(t){void 0!==this._$EC&&(this._$EC.forEach((t,e)=>this._$EO(e,this[e],t)),this._$EC=void 0),this._$Ek()}updated(t){}firstUpdated(t){}}var g;m.finalized=!0,m.elementProperties=new Map,m.elementStyles=[],m.shadowRootOptions={mode:"open"},null==_||_({ReactiveElement:m}),(null!==(h=d.reactiveElementVersions)&&void 0!==h?h:d.reactiveElementVersions=[]).push("1.6.3");const $=window,b=$.trustedTypes,E=b?b.createPolicy("lit-html",{createHTML:t=>t}):void 0,A=`lit$${(Math.random()+"").slice(9)}$`,w="?"+A,k=`<${w}>`,x=document,P=()=>x.createComment(""),j=t=>null===t||"object"!=typeof t&&"function"!=typeof t,O=Array.isArray,S=t=>O(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator]),C=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,M=/-->/g,D=/>/g,U=RegExp(">|[ \t\n\f\r](?:([^\\s\"'>=/]+)([ \t\n\f\r]*=[ \t\n\f\r]*(?:[^ \t\n\f\r\"'`<>=]|(\"|')|))|$)","g"),H=/'/g,T=/"/g,R=/^(?:script|style|textarea|title)$/i,B=t=>(e,...i)=>({_$litType$:t,strings:e,values:i}),L=B(1),I=(B(2),Symbol.for("lit-noChange")),K=Symbol.for("lit-nothing"),N=new WeakMap,z=x.createTreeWalker(x,129,null,!1);function W(t,e){if(!Array.isArray(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==E?E.createHTML(e):e}const V=(t,e)=>{const i=t.length-1,n=[];let s,o=2===e?"<svg>":"",r=C;for(let e=0;e<i;e++){const i=t[e];let a,l,c=-1,h=0;for(;h<i.length&&(r.lastIndex=h,l=r.exec(i),null!==l);)h=r.lastIndex,r===C?"!--"===l[1]?r=M:void 0!==l[1]?r=D:void 0!==l[2]?(R.test(l[2])&&(s=RegExp("</"+l[2],"g")),r=U):void 0!==l[3]&&(r=U):r===U?">"===l[0]?(r=null!=s?s:C,c=-1):void 0===l[1]?c=-2:(c=r.lastIndex-l[2].length,a=l[1],r=void 0===l[3]?U:'"'===l[3]?T:H):r===T||r===H?r=U:r===M||r===D?r=C:(r=U,s=void 0);const d=r===U&&t[e+1].startsWith("/>")?" ":"";o+=r===C?i+k:c>=0?(n.push(a),i.slice(0,c)+"$lit$"+i.slice(c)+A+d):i+A+(-2===c?(n.push(void 0),e):d)}return[W(t,o+(t[i]||"<?>")+(2===e?"</svg>":"")),n]};class q{constructor({strings:t,_$litType$:e},i){let n;this.parts=[];let s=0,o=0;const r=t.length-1,a=this.parts,[l,c]=V(t,e);if(this.el=q.createElement(l,i),z.currentNode=this.el.content,2===e){const t=this.el.content,e=t.firstChild;e.remove(),t.append(...e.childNodes)}for(;null!==(n=z.nextNode())&&a.length<r;){if(1===n.nodeType){if(n.hasAttributes()){const t=[];for(const e of n.getAttributeNames())if(e.endsWith("$lit$")||e.startsWith(A)){const i=c[o++];if(t.push(e),void 0!==i){const t=n.getAttribute(i.toLowerCase()+"$lit$").split(A),e=/([.?@])?(.*)/.exec(i);a.push({type:1,index:s,name:e[2],strings:t,ctor:"."===e[1]?Q:"?"===e[1]?Y:"@"===e[1]?tt:Z})}else a.push({type:6,index:s})}for(const e of t)n.removeAttribute(e)}if(R.test(n.tagName)){const t=n.textContent.split(A),e=t.length-1;if(e>0){n.textContent=b?b.emptyScript:"";for(let i=0;i<e;i++)n.append(t[i],P()),z.nextNode(),a.push({type:2,index:++s});n.append(t[e],P())}}}else if(8===n.nodeType)if(n.data===w)a.push({type:2,index:s});else{let t=-1;for(;-1!==(t=n.data.indexOf(A,t+1));)a.push({type:7,index:s}),t+=A.length-1}s++}}static createElement(t,e){const i=x.createElement("template");return i.innerHTML=t,i}}function F(t,e,i=t,n){var s,o,r,a;if(e===I)return e;let l=void 0!==n?null===(s=i._$Co)||void 0===s?void 0:s[n]:i._$Cl;const c=j(e)?void 0:e._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(o=null==l?void 0:l._$AO)||void 0===o||o.call(l,!1),void 0===c?l=void 0:(l=new c(t),l._$AT(t,i,n)),void 0!==n?(null!==(r=(a=i)._$Co)&&void 0!==r?r:a._$Co=[])[n]=l:i._$Cl=l),void 0!==l&&(e=F(t,l._$AS(t,e.values),l,n)),e}class J{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var e;const{el:{content:i},parts:n}=this._$AD,s=(null!==(e=null==t?void 0:t.creationScope)&&void 0!==e?e:x).importNode(i,!0);z.currentNode=s;let o=z.nextNode(),r=0,a=0,l=n[0];for(;void 0!==l;){if(r===l.index){let e;2===l.type?e=new G(o,o.nextSibling,this,t):1===l.type?e=new l.ctor(o,l.name,l.strings,this,t):6===l.type&&(e=new et(o,this,t)),this._$AV.push(e),l=n[++a]}r!==(null==l?void 0:l.index)&&(o=z.nextNode(),r++)}return z.currentNode=x,s}v(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class G{constructor(t,e,i,n){var s;this.type=2,this._$AH=K,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=n,this._$Cp=null===(s=null==n?void 0:n.isConnected)||void 0===s||s}get _$AU(){var t,e;return null!==(e=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==e?e:this._$Cp}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===(null==t?void 0:t.nodeType)&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=F(this,t,e),j(t)?t===K||null==t||""===t?(this._$AH!==K&&this._$AR(),this._$AH=K):t!==this._$AH&&t!==I&&this._(t):void 0!==t._$litType$?this.g(t):void 0!==t.nodeType?this.$(t):S(t)?this.T(t):this._(t)}k(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}$(t){this._$AH!==t&&(this._$AR(),this._$AH=this.k(t))}_(t){this._$AH!==K&&j(this._$AH)?this._$AA.nextSibling.data=t:this.$(x.createTextNode(t)),this._$AH=t}g(t){var e;const{values:i,_$litType$:n}=t,s="number"==typeof n?this._$AC(t):(void 0===n.el&&(n.el=q.createElement(W(n.h,n.h[0]),this.options)),n);if((null===(e=this._$AH)||void 0===e?void 0:e._$AD)===s)this._$AH.v(i);else{const t=new J(s,this),e=t.u(this.options);t.v(i),this.$(e),this._$AH=t}}_$AC(t){let e=N.get(t.strings);return void 0===e&&N.set(t.strings,e=new q(t)),e}T(t){O(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,n=0;for(const s of t)n===e.length?e.push(i=new G(this.k(P()),this.k(P()),this,this.options)):i=e[n],i._$AI(s),n++;n<e.length&&(this._$AR(i&&i._$AB.nextSibling,n),e.length=n)}_$AR(t=this._$AA.nextSibling,e){var i;for(null===(i=this._$AP)||void 0===i||i.call(this,!1,!0,e);t&&t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){var e;void 0===this._$AM&&(this._$Cp=t,null===(e=this._$AP)||void 0===e||e.call(this,t))}}class Z{constructor(t,e,i,n,s){this.type=1,this._$AH=K,this._$AN=void 0,this.element=t,this.name=e,this._$AM=n,this.options=s,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=K}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,e=this,i,n){const s=this.strings;let o=!1;if(void 0===s)t=F(this,t,e,0),o=!j(t)||t!==this._$AH&&t!==I,o&&(this._$AH=t);else{const n=t;let r,a;for(t=s[0],r=0;r<s.length-1;r++)a=F(this,n[i+r],e,r),a===I&&(a=this._$AH[r]),o||(o=!j(a)||a!==this._$AH[r]),a===K?t=K:t!==K&&(t+=(null!=a?a:"")+s[r+1]),this._$AH[r]=a}o&&!n&&this.j(t)}j(t){t===K?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"")}}class Q extends Z{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===K?void 0:t}}const X=b?b.emptyScript:"";class Y extends Z{constructor(){super(...arguments),this.type=4}j(t){t&&t!==K?this.element.setAttribute(this.name,X):this.element.removeAttribute(this.name)}}class tt extends Z{constructor(t,e,i,n,s){super(t,e,i,n,s),this.type=5}_$AI(t,e=this){var i;if((t=null!==(i=F(this,t,e,0))&&void 0!==i?i:K)===I)return;const n=this._$AH,s=t===K&&n!==K||t.capture!==n.capture||t.once!==n.once||t.passive!==n.passive,o=t!==K&&(n===K||s);s&&this.element.removeEventListener(this.name,this,n),o&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e,i;"function"==typeof this._$AH?this._$AH.call(null!==(i=null===(e=this.options)||void 0===e?void 0:e.host)&&void 0!==i?i:this.element,t):this._$AH.handleEvent(t)}}class et{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){F(this,t)}}const it={O:"$lit$",P:A,A:w,C:1,M:V,L:J,R:S,D:F,I:G,V:Z,H:Y,N:tt,U:Q,F:et},nt=$.litHtmlPolyfillSupport;null==nt||nt(q,G),(null!==(g=$.litHtmlVersions)&&void 0!==g?g:$.litHtmlVersions=[]).push("2.8.0");var st,ot;class rt extends m{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{var n,s;const o=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:e;let r=o._$litPart$;if(void 0===r){const t=null!==(s=null==i?void 0:i.renderBefore)&&void 0!==s?s:null;o._$litPart$=r=new G(e.insertBefore(P(),t),t,void 0,null!=i?i:{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!1)}render(){return I}}rt.finalized=!0,rt._$litElement$=!0,null===(st=globalThis.litElementHydrateSupport)||void 0===st||st.call(globalThis,{LitElement:rt});const at=globalThis.litElementPolyfillSupport;null==at||at({LitElement:rt});(null!==(ot=globalThis.litElementVersions)&&void 0!==ot?ot:globalThis.litElementVersions=[]).push("3.3.3");const lt=t=>e=>"function"==typeof e?((t,e)=>(customElements.define(t,e),e))(t,e):((t,e)=>{const{kind:i,elements:n}=e;return{kind:i,elements:n,finisher(e){customElements.define(t,e)}}})(t,e),ct=(t,e)=>"method"===e.kind&&e.descriptor&&!("value"in e.descriptor)?{...e,finisher(i){i.createProperty(e.key,t)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:e.key,initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this))},finisher(i){i.createProperty(e.key,t)}};function ht(t){return(e,i)=>void 0!==i?((t,e,i)=>{e.constructor.createProperty(i,t)})(t,e,i):ct(t,e)}function dt(t){return ht({...t,state:!0})}var pt;null===(pt=window.HTMLSlotElement)||void 0===pt||pt.prototype.assignedElements;const ut=1,_t=2,ft=3,vt=4,yt=t=>(...e)=>({_$litDirective$:t,values:e});class mt{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}const{I:gt}=it,$t=t=>void 0===t.strings,bt=()=>document.createComment(""),Et=(t,e,i)=>{var n;const s=t._$AA.parentNode,o=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=s.insertBefore(bt(),o),n=s.insertBefore(bt(),o);i=new gt(e,n,t,t.options)}else{const e=i._$AB.nextSibling,r=i._$AM,a=r!==t;if(a){let e;null===(n=i._$AQ)||void 0===n||n.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==r._$AU&&i._$AP(e)}if(e!==o||a){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;s.insertBefore(t,o),t=e}}}return i},At=(t,e,i=t)=>(t._$AI(e,i),t),wt={},kt=(t,e=wt)=>t._$AH=e,xt=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const n=t._$AB.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},Pt=(t,e,i)=>{const n=new Map;for(let s=e;s<=i;s++)n.set(t[s],s);return n},jt=yt(class extends mt{constructor(t){if(super(t),t.type!==_t)throw Error("repeat() can only be used in text expressions")}ct(t,e,i){let n;void 0===i?i=e:void 0!==e&&(n=e);const s=[],o=[];let r=0;for(const e of t)s[r]=n?n(e,r):r,o[r]=i(e,r),r++;return{values:o,keys:s}}render(t,e,i){return this.ct(t,e,i).values}update(t,[e,i,n]){var s;const o=t._$AH,{values:r,keys:a}=this.ct(e,i,n);if(!Array.isArray(o))return this.ut=a,r;const l=null!==(s=this.ut)&&void 0!==s?s:this.ut=[],c=[];let h,d,p=0,u=o.length-1,_=0,f=r.length-1;for(;p<=u&&_<=f;)if(null===o[p])p++;else if(null===o[u])u--;else if(l[p]===a[_])c[_]=At(o[p],r[_]),p++,_++;else if(l[u]===a[f])c[f]=At(o[u],r[f]),u--,f--;else if(l[p]===a[f])c[f]=At(o[p],r[f]),Et(t,c[f+1],o[p]),p++,f--;else if(l[u]===a[_])c[_]=At(o[u],r[_]),Et(t,o[p],o[u]),u--,_++;else if(void 0===h&&(h=Pt(a,_,f),d=Pt(l,p,u)),h.has(l[p]))if(h.has(l[u])){const e=d.get(a[_]),i=void 0!==e?o[e]:null;if(null===i){const e=Et(t,o[p]);At(e,r[_]),c[_]=e}else c[_]=At(i,r[_]),Et(t,o[p],i),o[e]=null;_++}else xt(o[u]),u--;else xt(o[p]),p++;for(;_<=f;){const e=Et(t,c[f+1]);At(e,r[_]),c[_++]=e}for(;p<=u;){const t=o[p++];null!==t&&xt(t)}return this.ut=a,kt(t,c),I}}),Ot=yt(class extends mt{constructor(t){if(super(t),t.type!==ft&&t.type!==ut&&t.type!==vt)throw Error("The `live` directive is not allowed on child or event bindings");if(!$t(t))throw Error("`live` bindings can only contain a single expression")}render(t){return t}update(t,[e]){if(e===I||e===K)return e;const i=t.element,n=t.name;if(t.type===ft){if(e===i[n])return I}else if(t.type===vt){if(!!e===i.hasAttribute(n))return I}else if(t.type===ut&&i.getAttribute(n)===e+"")return I;return kt(t),e}}),St=(t,e)=>{var i,n;const s=t._$AN;if(void 0===s)return!1;for(const t of s)null===(n=(i=t)._$AO)||void 0===n||n.call(i,e,!1),St(t,e);return!0},Ct=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},Mt=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),Ht(e)}};function Dt(t){void 0!==this._$AN?(Ct(this),this._$AM=t,Mt(this)):this._$AM=t}function Ut(t,e=!1,i=0){const n=this._$AH,s=this._$AN;if(void 0!==s&&0!==s.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)St(n[t],!1),Ct(n[t]);else null!=n&&(St(n,!1),Ct(n));else St(this,t)}const Ht=t=>{var e,i,n,s;t.type==_t&&(null!==(e=(n=t)._$AP)&&void 0!==e||(n._$AP=Ut),null!==(i=(s=t)._$AQ)&&void 0!==i||(s._$AQ=Dt))};class Tt extends mt{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),Mt(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,n;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),e&&(St(this,t),Ct(this))}setValue(t){if($t(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}const Rt=()=>new Bt;class Bt{}const Lt=new WeakMap,It=yt(class extends Tt{render(t){return K}update(t,[e]){var i;const n=e!==this.G;return n&&void 0!==this.G&&this.ot(void 0),(n||this.rt!==this.lt)&&(this.G=e,this.dt=null===(i=t.options)||void 0===i?void 0:i.host,this.ot(this.lt=t.element)),K}ot(t){var e;if("function"==typeof this.G){const i=null!==(e=this.dt)&&void 0!==e?e:globalThis;let n=Lt.get(i);void 0===n&&(n=new WeakMap,Lt.set(i,n)),void 0!==n.get(this.G)&&this.G.call(this.dt,void 0),n.set(this.G,t),void 0!==t&&this.G.call(this.dt,t)}else this.G.value=t}get rt(){var t,e,i;return"function"==typeof this.G?null===(e=Lt.get(null!==(t=this.dt)&&void 0!==t?t:globalThis))||void 0===e?void 0:e.get(this.G):null===(i=this.G)||void 0===i?void 0:i.value}disconnected(){this.rt===this.lt&&this.ot(void 0)}reconnected(){this.ot(this.lt)}}),Kt=yt(class extends mt{constructor(t){var e;if(super(t),t.type!==ut||"class"!==t.name||(null===(e=t.strings)||void 0===e?void 0:e.length)>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(t){return" "+Object.keys(t).filter(e=>t[e]).join(" ")+" "}update(t,[e]){var i,n;if(void 0===this.it){this.it=new Set,void 0!==t.strings&&(this.nt=new Set(t.strings.join(" ").split(/\s/).filter(t=>""!==t)));for(const t in e)e[t]&&!(null===(i=this.nt)||void 0===i?void 0:i.has(t))&&this.it.add(t);return this.render(e)}const s=t.element.classList;this.it.forEach(t=>{t in e||(s.remove(t),this.it.delete(t))});for(const t in e){const i=!!e[t];i===this.it.has(t)||(null===(n=this.nt)||void 0===n?void 0:n.has(t))||(i?(s.add(t),this.it.add(t)):(s.remove(t),this.it.delete(t)))}return I}});var Nt="undefined"!=typeof navigator&&navigator.userAgent.toLowerCase().indexOf("firefox")>0;function zt(t,e,i){t.addEventListener?t.addEventListener(e,i,!1):t.attachEvent&&t.attachEvent("on".concat(e),(function(){i(window.event)}))}function Wt(t,e){for(var i=e.slice(0,e.length-1),n=0;n<i.length;n++)i[n]=t[i[n].toLowerCase()];return i}function Vt(t){"string"!=typeof t&&(t="");for(var e=(t=t.replace(/\s/g,"")).split(","),i=e.lastIndexOf("");i>=0;)e[i-1]+=",",e.splice(i,1),i=e.lastIndexOf("");return e}for(var qt={backspace:8,tab:9,clear:12,enter:13,return:13,esc:27,escape:27,space:32,left:37,up:38,right:39,down:40,del:46,delete:46,ins:45,insert:45,home:36,end:35,pageup:33,pagedown:34,capslock:20,num_0:96,num_1:97,num_2:98,num_3:99,num_4:100,num_5:101,num_6:102,num_7:103,num_8:104,num_9:105,num_multiply:106,num_add:107,num_enter:108,num_subtract:109,num_decimal:110,num_divide:111,"⇪":20,",":188,".":190,"/":191,"`":192,"-":Nt?173:189,"=":Nt?61:187,";":Nt?59:186,"'":222,"[":219,"]":221,"\\":220},Ft={"⇧":16,shift:16,"⌥":18,alt:18,option:18,"⌃":17,ctrl:17,control:17,"⌘":91,cmd:91,command:91},Jt={16:"shiftKey",18:"altKey",17:"ctrlKey",91:"metaKey",shiftKey:16,ctrlKey:17,altKey:18,metaKey:91},Gt={16:!1,18:!1,17:!1,91:!1},Zt={},Qt=1;Qt<20;Qt++)qt["f".concat(Qt)]=111+Qt;var Xt=[],Yt="all",te=[],ee=function(t){return qt[t.toLowerCase()]||Ft[t.toLowerCase()]||t.toUpperCase().charCodeAt(0)};function ie(t){Yt=t||"all"}function ne(){return Yt||"all"}var se=function(t){var e=t.key,i=t.scope,n=t.method,s=t.splitKey,o=void 0===s?"+":s;Vt(e).forEach((function(t){var e=t.split(o),s=e.length,r=e[s-1],a="*"===r?"*":ee(r);if(Zt[a]){i||(i=ne());var l=s>1?Wt(Ft,e):[];Zt[a]=Zt[a].map((function(t){return(!n||t.method===n)&&t.scope===i&&function(t,e){for(var i=t.length>=e.length?t:e,n=t.length>=e.length?e:t,s=!0,o=0;o<i.length;o++)-1===n.indexOf(i[o])&&(s=!1);return s}(t.mods,l)?{}:t}))}}))};function oe(t,e,i){var n;if(e.scope===i||"all"===e.scope){for(var s in n=e.mods.length>0,Gt)Object.prototype.hasOwnProperty.call(Gt,s)&&(!Gt[s]&&e.mods.indexOf(+s)>-1||Gt[s]&&-1===e.mods.indexOf(+s))&&(n=!1);(0!==e.mods.length||Gt[16]||Gt[18]||Gt[17]||Gt[91])&&!n&&"*"!==e.shortcut||!1===e.method(t,e)&&(t.preventDefault?t.preventDefault():t.returnValue=!1,t.stopPropagation&&t.stopPropagation(),t.cancelBubble&&(t.cancelBubble=!0))}}function re(t){var e=Zt["*"],i=t.keyCode||t.which||t.charCode;if(ae.filter.call(this,t)){if(93!==i&&224!==i||(i=91),-1===Xt.indexOf(i)&&229!==i&&Xt.push(i),["ctrlKey","altKey","shiftKey","metaKey"].forEach((function(e){var i=Jt[e];t[e]&&-1===Xt.indexOf(i)?Xt.push(i):!t[e]&&Xt.indexOf(i)>-1?Xt.splice(Xt.indexOf(i),1):"metaKey"===e&&t[e]&&3===Xt.length&&(t.ctrlKey||t.shiftKey||t.altKey||(Xt=Xt.slice(Xt.indexOf(i))))})),i in Gt){for(var n in Gt[i]=!0,Ft)Ft[n]===i&&(ae[n]=!0);if(!e)return}for(var s in Gt)Object.prototype.hasOwnProperty.call(Gt,s)&&(Gt[s]=t[Jt[s]]);t.getModifierState&&(!t.altKey||t.ctrlKey)&&t.getModifierState("AltGraph")&&(-1===Xt.indexOf(17)&&Xt.push(17),-1===Xt.indexOf(18)&&Xt.push(18),Gt[17]=!0,Gt[18]=!0);var o=ne();if(e)for(var r=0;r<e.length;r++)e[r].scope===o&&("keydown"===t.type&&e[r].keydown||"keyup"===t.type&&e[r].keyup)&&oe(t,e[r],o);if(i in Zt)for(var a=0;a<Zt[i].length;a++)if(("keydown"===t.type&&Zt[i][a].keydown||"keyup"===t.type&&Zt[i][a].keyup)&&Zt[i][a].key){for(var l=Zt[i][a],c=l.splitKey,h=l.key.split(c),d=[],p=0;p<h.length;p++)d.push(ee(h[p]));d.sort().join("")===Xt.sort().join("")&&oe(t,l,o)}}}function ae(t,e,i){Xt=[];var n=Vt(t),s=[],o="all",r=document,a=0,l=!1,c=!0,h="+";for(void 0===i&&"function"==typeof e&&(i=e),"[object Object]"===Object.prototype.toString.call(e)&&(e.scope&&(o=e.scope),e.element&&(r=e.element),e.keyup&&(l=e.keyup),void 0!==e.keydown&&(c=e.keydown),"string"==typeof e.splitKey&&(h=e.splitKey)),"string"==typeof e&&(o=e);a<n.length;a++)s=[],(t=n[a].split(h)).length>1&&(s=Wt(Ft,t)),(t="*"===(t=t[t.length-1])?"*":ee(t))in Zt||(Zt[t]=[]),Zt[t].push({keyup:l,keydown:c,scope:o,mods:s,shortcut:n[a],method:i,key:n[a],splitKey:h});void 0!==r&&!function(t){return te.indexOf(t)>-1}(r)&&window&&(te.push(r),zt(r,"keydown",(function(t){re(t)})),zt(window,"focus",(function(){Xt=[]})),zt(r,"keyup",(function(t){re(t),function(t){var e=t.keyCode||t.which||t.charCode,i=Xt.indexOf(e);if(i>=0&&Xt.splice(i,1),t.key&&"meta"===t.key.toLowerCase()&&Xt.splice(0,Xt.length),93!==e&&224!==e||(e=91),e in Gt)for(var n in Gt[e]=!1,Ft)Ft[n]===e&&(ae[n]=!1)}(t)})))}var le={setScope:ie,getScope:ne,deleteScope:function(t,e){var i,n;for(var s in t||(t=ne()),Zt)if(Object.prototype.hasOwnProperty.call(Zt,s))for(i=Zt[s],n=0;n<i.length;)i[n].scope===t?i.splice(n,1):n++;ne()===t&&ie(e||"all")},getPressedKeyCodes:function(){return Xt.slice(0)},isPressed:function(t){return"string"==typeof t&&(t=ee(t)),-1!==Xt.indexOf(t)},filter:function(t){var e=t.target||t.srcElement,i=e.tagName,n=!0;return!e.isContentEditable&&("INPUT"!==i&&"TEXTAREA"!==i&&"SELECT"!==i||e.readOnly)||(n=!1),n},unbind:function(t){if(t){if(Array.isArray(t))t.forEach((function(t){t.key&&se(t)}));else if("object"==typeof t)t.key&&se(t);else if("string"==typeof t){for(var e=arguments.length,i=new Array(e>1?e-1:0),n=1;n<e;n++)i[n-1]=arguments[n];var s=i[0],o=i[1];"function"==typeof s&&(o=s,s=""),se({key:t,scope:s,method:o,splitKey:"+"})}}else Object.keys(Zt).forEach((function(t){return delete Zt[t]}))}};for(var ce in le)Object.prototype.hasOwnProperty.call(le,ce)&&(ae[ce]=le[ce]);if("undefined"!=typeof window){var he=window.hotkeys;ae.noConflict=function(t){return t&&window.hotkeys===ae&&(window.hotkeys=he),ae},window.hotkeys=ae}var de=ae,pe=function(t,e,i,n){var s,o=arguments.length,r=o<3?e:null===n?n=Object.getOwnPropertyDescriptor(e,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,n);else for(var a=t.length-1;a>=0;a--)(s=t[a])&&(r=(o<3?s(r):o>3?s(e,i,r):s(e,i))||r);return o>3&&r&&Object.defineProperty(e,i,r),r};let ue=class extends rt{constructor(){super(...arguments),this.placeholder="",this.hideBreadcrumbs=!1,this.breadcrumbHome="Home",this.breadcrumbs=[],this._inputRef=Rt()}render(){let t="";if(!this.hideBreadcrumbs){const e=[];for(const t of this.breadcrumbs)e.push(L`<button
            tabindex="-1"
            @click=${()=>this.selectParent(t)}
            class="breadcrumb"
          >
            ${t}
          </button>`);t=L`<div class="breadcrumb-list">
        <button
          tabindex="-1"
          @click=${()=>this.selectParent()}
          class="breadcrumb"
        >
          ${this.breadcrumbHome}
        </button>
        ${e}
      </div>`}return L`
      ${t}
      <div part="ninja-input-wrapper" class="search-wrapper">
        <input
          part="ninja-input"
          type="text"
          id="search"
          spellcheck="false"
          autocomplete="off"
          @input="${this._handleInput}"
          ${It(this._inputRef)}
          placeholder="${this.placeholder}"
          class="search"
        />
      </div>
    `}setSearch(t){this._inputRef.value&&(this._inputRef.value.value=t)}focusSearch(){requestAnimationFrame(()=>this._inputRef.value.focus())}_handleInput(t){const e=t.target;this.dispatchEvent(new CustomEvent("change",{detail:{search:e.value},bubbles:!1,composed:!1}))}selectParent(t){this.dispatchEvent(new CustomEvent("setParent",{detail:{parent:t},bubbles:!0,composed:!0}))}firstUpdated(){this.focusSearch()}_close(){this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}};ue.styles=l`
    :host {
      flex: 1;
      position: relative;
    }
    .search {
      padding: 1.25em;
      flex-grow: 1;
      flex-shrink: 0;
      margin: 0px;
      border: none;
      appearance: none;
      font-size: 1.125em;
      background: transparent;
      caret-color: var(--ninja-accent-color);
      color: var(--ninja-text-color);
      outline: none;
      font-family: var(--ninja-font-family);
    }
    .search::placeholder {
      color: var(--ninja-placeholder-color);
    }
    .breadcrumb-list {
      padding: 1em 4em 0 1em;
      display: flex;
      flex-direction: row;
      align-items: stretch;
      justify-content: flex-start;
      flex: initial;
    }

    .breadcrumb {
      background: var(--ninja-secondary-background-color);
      text-align: center;
      line-height: 1.2em;
      border-radius: var(--ninja-key-border-radius);
      border: 0;
      cursor: pointer;
      padding: 0.1em 0.5em;
      color: var(--ninja-secondary-text-color);
      margin-right: 0.5em;
      outline: none;
      font-family: var(--ninja-font-family);
    }

    .search-wrapper {
      display: flex;
      border-bottom: var(--ninja-separate-border);
    }
  `,pe([ht()],ue.prototype,"placeholder",void 0),pe([ht({type:Boolean})],ue.prototype,"hideBreadcrumbs",void 0),pe([ht()],ue.prototype,"breadcrumbHome",void 0),pe([ht({type:Array})],ue.prototype,"breadcrumbs",void 0),ue=pe([lt("ninja-header")],ue);class _e extends mt{constructor(t){if(super(t),this.et=K,t.type!==_t)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===K||null==t)return this.ft=void 0,this.et=t;if(t===I)return t;if("string"!=typeof t)throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.et)return this.ft;this.et=t;const e=[t];return e.raw=e,this.ft={_$litType$:this.constructor.resultType,strings:e,values:[]}}}_e.directiveName="unsafeHTML",_e.resultType=1;const fe=yt(_e);var ve=i(2);const ye=window,me=ye.ShadowRoot&&(void 0===ye.ShadyCSS||ye.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,ge=Symbol(),$e=new WeakMap;class be{constructor(t,e,i){if(this._$cssResult$=!0,i!==ge)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(me&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=$e.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&$e.set(e,t))}return t}toString(){return this.cssText}}const Ee=me?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new be("string"==typeof t?t:t+"",void 0,ge))(e)})(t):t;var Ae;const we=window,ke=we.trustedTypes,xe=ke?ke.emptyScript:"",Pe=we.reactiveElementPolyfillSupport,je={toAttribute(t,e){switch(e){case Boolean:t=t?xe:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},Oe=(t,e)=>e!==t&&(e==e||t==t),Se={attribute:!0,type:String,converter:je,reflect:!1,hasChanged:Oe};class Ce extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(t){var e;this.finalize(),(null!==(e=this.h)&&void 0!==e?e:this.h=[]).push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach((e,i)=>{const n=this._$Ep(i,e);void 0!==n&&(this._$Ev.set(n,i),t.push(n))}),t}static createProperty(t,e=Se){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const i="symbol"==typeof t?Symbol():"__"+t,n=this.getPropertyDescriptor(t,i,e);void 0!==n&&Object.defineProperty(this.prototype,t,n)}}static getPropertyDescriptor(t,e,i){return{get(){return this[e]},set(n){const s=this[t];this[e]=n,this.requestUpdate(t,s,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||Se}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),void 0!==t.h&&(this.h=[...t.h]),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,e=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const i of e)this.createProperty(i,t[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(Ee(t))}else void 0!==t&&e.push(Ee(t));return e}static _$Ep(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}_$Eu(){var t;this._$E_=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null===(t=this.constructor.h)||void 0===t||t.forEach(t=>t(this))}addController(t){var e,i;(null!==(e=this._$ES)&&void 0!==e?e:this._$ES=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(i=t.hostConnected)||void 0===i||i.call(t))}removeController(t){var e;null===(e=this._$ES)||void 0===e||e.splice(this._$ES.indexOf(t)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((t,e)=>{this.hasOwnProperty(e)&&(this._$Ei.set(e,this[e]),delete this[e])})}createRenderRoot(){var t;const e=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return((t,e)=>{me?t.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet):e.forEach(e=>{const i=document.createElement("style"),n=ye.litNonce;void 0!==n&&i.setAttribute("nonce",n),i.textContent=e.cssText,t.appendChild(i)})})(e,this.constructor.elementStyles),e}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostConnected)||void 0===e?void 0:e.call(t)})}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostDisconnected)||void 0===e?void 0:e.call(t)})}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$EO(t,e,i=Se){var n;const s=this.constructor._$Ep(t,i);if(void 0!==s&&!0===i.reflect){const o=(void 0!==(null===(n=i.converter)||void 0===n?void 0:n.toAttribute)?i.converter:je).toAttribute(e,i.type);this._$El=t,null==o?this.removeAttribute(s):this.setAttribute(s,o),this._$El=null}}_$AK(t,e){var i;const n=this.constructor,s=n._$Ev.get(t);if(void 0!==s&&this._$El!==s){const t=n.getPropertyOptions(s),o="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==(null===(i=t.converter)||void 0===i?void 0:i.fromAttribute)?t.converter:je;this._$El=s,this[s]=o.fromAttribute(e,t.type),this._$El=null}}requestUpdate(t,e,i){let n=!0;void 0!==t&&(((i=i||this.constructor.getPropertyOptions(t)).hasChanged||Oe)(this[t],e)?(this._$AL.has(t)||this._$AL.set(t,e),!0===i.reflect&&this._$El!==t&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(t,i))):n=!1),!this.isUpdatePending&&n&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach((t,e)=>this[e]=t),this._$Ei=void 0);let e=!1;const i=this._$AL;try{e=this.shouldUpdate(i),e?(this.willUpdate(i),null===(t=this._$ES)||void 0===t||t.forEach(t=>{var e;return null===(e=t.hostUpdate)||void 0===e?void 0:e.call(t)}),this.update(i)):this._$Ek()}catch(t){throw e=!1,this._$Ek(),t}e&&this._$AE(i)}willUpdate(t){}_$AE(t){var e;null===(e=this._$ES)||void 0===e||e.forEach(t=>{var e;return null===(e=t.hostUpdated)||void 0===e?void 0:e.call(t)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return!0}update(t){void 0!==this._$EC&&(this._$EC.forEach((t,e)=>this._$EO(e,this[e],t)),this._$EC=void 0),this._$Ek()}updated(t){}firstUpdated(t){}}var Me;Ce.finalized=!0,Ce.elementProperties=new Map,Ce.elementStyles=[],Ce.shadowRootOptions={mode:"open"},null==Pe||Pe({ReactiveElement:Ce}),(null!==(Ae=we.reactiveElementVersions)&&void 0!==Ae?Ae:we.reactiveElementVersions=[]).push("1.6.3");const De=window,Ue=De.trustedTypes,He=Ue?Ue.createPolicy("lit-html",{createHTML:t=>t}):void 0,Te=`lit$${(Math.random()+"").slice(9)}$`,Re="?"+Te,Be=`<${Re}>`,Le=document,Ie=()=>Le.createComment(""),Ke=t=>null===t||"object"!=typeof t&&"function"!=typeof t,Ne=Array.isArray,ze=t=>Ne(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator]),We=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Ve=/-->/g,qe=/>/g,Fe=RegExp(">|[ \t\n\f\r](?:([^\\s\"'>=/]+)([ \t\n\f\r]*=[ \t\n\f\r]*(?:[^ \t\n\f\r\"'`<>=]|(\"|')|))|$)","g"),Je=/'/g,Ge=/"/g,Ze=/^(?:script|style|textarea|title)$/i,Qe=t=>(e,...i)=>({_$litType$:t,strings:e,values:i}),Xe=Qe(1),Ye=(Qe(2),Symbol.for("lit-noChange")),ti=Symbol.for("lit-nothing"),ei=new WeakMap,ii=Le.createTreeWalker(Le,129,null,!1);function ni(t,e){if(!Array.isArray(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==He?He.createHTML(e):e}const si=(t,e)=>{const i=t.length-1,n=[];let s,o=2===e?"<svg>":"",r=We;for(let e=0;e<i;e++){const i=t[e];let a,l,c=-1,h=0;for(;h<i.length&&(r.lastIndex=h,l=r.exec(i),null!==l);)h=r.lastIndex,r===We?"!--"===l[1]?r=Ve:void 0!==l[1]?r=qe:void 0!==l[2]?(Ze.test(l[2])&&(s=RegExp("</"+l[2],"g")),r=Fe):void 0!==l[3]&&(r=Fe):r===Fe?">"===l[0]?(r=null!=s?s:We,c=-1):void 0===l[1]?c=-2:(c=r.lastIndex-l[2].length,a=l[1],r=void 0===l[3]?Fe:'"'===l[3]?Ge:Je):r===Ge||r===Je?r=Fe:r===Ve||r===qe?r=We:(r=Fe,s=void 0);const d=r===Fe&&t[e+1].startsWith("/>")?" ":"";o+=r===We?i+Be:c>=0?(n.push(a),i.slice(0,c)+"$lit$"+i.slice(c)+Te+d):i+Te+(-2===c?(n.push(void 0),e):d)}return[ni(t,o+(t[i]||"<?>")+(2===e?"</svg>":"")),n]};class oi{constructor({strings:t,_$litType$:e},i){let n;this.parts=[];let s=0,o=0;const r=t.length-1,a=this.parts,[l,c]=si(t,e);if(this.el=oi.createElement(l,i),ii.currentNode=this.el.content,2===e){const t=this.el.content,e=t.firstChild;e.remove(),t.append(...e.childNodes)}for(;null!==(n=ii.nextNode())&&a.length<r;){if(1===n.nodeType){if(n.hasAttributes()){const t=[];for(const e of n.getAttributeNames())if(e.endsWith("$lit$")||e.startsWith(Te)){const i=c[o++];if(t.push(e),void 0!==i){const t=n.getAttribute(i.toLowerCase()+"$lit$").split(Te),e=/([.?@])?(.*)/.exec(i);a.push({type:1,index:s,name:e[2],strings:t,ctor:"."===e[1]?hi:"?"===e[1]?pi:"@"===e[1]?ui:ci})}else a.push({type:6,index:s})}for(const e of t)n.removeAttribute(e)}if(Ze.test(n.tagName)){const t=n.textContent.split(Te),e=t.length-1;if(e>0){n.textContent=Ue?Ue.emptyScript:"";for(let i=0;i<e;i++)n.append(t[i],Ie()),ii.nextNode(),a.push({type:2,index:++s});n.append(t[e],Ie())}}}else if(8===n.nodeType)if(n.data===Re)a.push({type:2,index:s});else{let t=-1;for(;-1!==(t=n.data.indexOf(Te,t+1));)a.push({type:7,index:s}),t+=Te.length-1}s++}}static createElement(t,e){const i=Le.createElement("template");return i.innerHTML=t,i}}function ri(t,e,i=t,n){var s,o,r,a;if(e===Ye)return e;let l=void 0!==n?null===(s=i._$Co)||void 0===s?void 0:s[n]:i._$Cl;const c=Ke(e)?void 0:e._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(o=null==l?void 0:l._$AO)||void 0===o||o.call(l,!1),void 0===c?l=void 0:(l=new c(t),l._$AT(t,i,n)),void 0!==n?(null!==(r=(a=i)._$Co)&&void 0!==r?r:a._$Co=[])[n]=l:i._$Cl=l),void 0!==l&&(e=ri(t,l._$AS(t,e.values),l,n)),e}class ai{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var e;const{el:{content:i},parts:n}=this._$AD,s=(null!==(e=null==t?void 0:t.creationScope)&&void 0!==e?e:Le).importNode(i,!0);ii.currentNode=s;let o=ii.nextNode(),r=0,a=0,l=n[0];for(;void 0!==l;){if(r===l.index){let e;2===l.type?e=new li(o,o.nextSibling,this,t):1===l.type?e=new l.ctor(o,l.name,l.strings,this,t):6===l.type&&(e=new _i(o,this,t)),this._$AV.push(e),l=n[++a]}r!==(null==l?void 0:l.index)&&(o=ii.nextNode(),r++)}return ii.currentNode=Le,s}v(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class li{constructor(t,e,i,n){var s;this.type=2,this._$AH=ti,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=n,this._$Cp=null===(s=null==n?void 0:n.isConnected)||void 0===s||s}get _$AU(){var t,e;return null!==(e=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==e?e:this._$Cp}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===(null==t?void 0:t.nodeType)&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=ri(this,t,e),Ke(t)?t===ti||null==t||""===t?(this._$AH!==ti&&this._$AR(),this._$AH=ti):t!==this._$AH&&t!==Ye&&this._(t):void 0!==t._$litType$?this.g(t):void 0!==t.nodeType?this.$(t):ze(t)?this.T(t):this._(t)}k(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}$(t){this._$AH!==t&&(this._$AR(),this._$AH=this.k(t))}_(t){this._$AH!==ti&&Ke(this._$AH)?this._$AA.nextSibling.data=t:this.$(Le.createTextNode(t)),this._$AH=t}g(t){var e;const{values:i,_$litType$:n}=t,s="number"==typeof n?this._$AC(t):(void 0===n.el&&(n.el=oi.createElement(ni(n.h,n.h[0]),this.options)),n);if((null===(e=this._$AH)||void 0===e?void 0:e._$AD)===s)this._$AH.v(i);else{const t=new ai(s,this),e=t.u(this.options);t.v(i),this.$(e),this._$AH=t}}_$AC(t){let e=ei.get(t.strings);return void 0===e&&ei.set(t.strings,e=new oi(t)),e}T(t){Ne(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,n=0;for(const s of t)n===e.length?e.push(i=new li(this.k(Ie()),this.k(Ie()),this,this.options)):i=e[n],i._$AI(s),n++;n<e.length&&(this._$AR(i&&i._$AB.nextSibling,n),e.length=n)}_$AR(t=this._$AA.nextSibling,e){var i;for(null===(i=this._$AP)||void 0===i||i.call(this,!1,!0,e);t&&t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){var e;void 0===this._$AM&&(this._$Cp=t,null===(e=this._$AP)||void 0===e||e.call(this,t))}}class ci{constructor(t,e,i,n,s){this.type=1,this._$AH=ti,this._$AN=void 0,this.element=t,this.name=e,this._$AM=n,this.options=s,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=ti}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,e=this,i,n){const s=this.strings;let o=!1;if(void 0===s)t=ri(this,t,e,0),o=!Ke(t)||t!==this._$AH&&t!==Ye,o&&(this._$AH=t);else{const n=t;let r,a;for(t=s[0],r=0;r<s.length-1;r++)a=ri(this,n[i+r],e,r),a===Ye&&(a=this._$AH[r]),o||(o=!Ke(a)||a!==this._$AH[r]),a===ti?t=ti:t!==ti&&(t+=(null!=a?a:"")+s[r+1]),this._$AH[r]=a}o&&!n&&this.j(t)}j(t){t===ti?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"")}}class hi extends ci{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===ti?void 0:t}}const di=Ue?Ue.emptyScript:"";class pi extends ci{constructor(){super(...arguments),this.type=4}j(t){t&&t!==ti?this.element.setAttribute(this.name,di):this.element.removeAttribute(this.name)}}class ui extends ci{constructor(t,e,i,n,s){super(t,e,i,n,s),this.type=5}_$AI(t,e=this){var i;if((t=null!==(i=ri(this,t,e,0))&&void 0!==i?i:ti)===Ye)return;const n=this._$AH,s=t===ti&&n!==ti||t.capture!==n.capture||t.once!==n.once||t.passive!==n.passive,o=t!==ti&&(n===ti||s);s&&this.element.removeEventListener(this.name,this,n),o&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e,i;"function"==typeof this._$AH?this._$AH.call(null!==(i=null===(e=this.options)||void 0===e?void 0:e.host)&&void 0!==i?i:this.element,t):this._$AH.handleEvent(t)}}class _i{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){ri(this,t)}}const fi=De.litHtmlPolyfillSupport;null==fi||fi(oi,li),(null!==(Me=De.litHtmlVersions)&&void 0!==Me?Me:De.litHtmlVersions=[]).push("2.8.0");var vi,yi;class mi extends Ce{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{var n,s;const o=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:e;let r=o._$litPart$;if(void 0===r){const t=null!==(s=null==i?void 0:i.renderBefore)&&void 0!==s?s:null;o._$litPart$=r=new li(e.insertBefore(Ie(),t),t,void 0,null!=i?i:{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!1)}render(){return Ye}}mi.finalized=!0,mi._$litElement$=!0,null===(vi=globalThis.litElementHydrateSupport)||void 0===vi||vi.call(globalThis,{LitElement:mi});const gi=globalThis.litElementPolyfillSupport;null==gi||gi({LitElement:mi});(null!==(yi=globalThis.litElementVersions)&&void 0!==yi?yi:globalThis.litElementVersions=[]).push("3.3.3");var $i;null===($i=window.HTMLSlotElement)||void 0===$i||$i.prototype.assignedElements;const bi=((t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,n)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[n+1],t[0]);return new be(i,t,ge)})`:host{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}`;let Ei=class extends mi{render(){return Xe`<span><slot></slot></span>`}};var Ai;Ei.styles=[bi],Ei=Object(ve.c)([(Ai="mwc-icon",t=>"function"==typeof t?((t,e)=>(customElements.define(t,e),e))(Ai,t):((t,e)=>{const{kind:i,elements:n}=e;return{kind:i,elements:n,finisher(e){customElements.define(t,e)}}})(Ai,t))],Ei);var wi=function(t,e,i,n){var s,o=arguments.length,r=o<3?e:null===n?n=Object.getOwnPropertyDescriptor(e,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,n);else for(var a=t.length-1;a>=0;a--)(s=t[a])&&(r=(o<3?s(r):o>3?s(e,i,r):s(e,i))||r);return o>3&&r&&Object.defineProperty(e,i,r),r};let ki=class extends rt{constructor(){super(),this.selected=!1,this.hotKeysJoinedView=!0,this.addEventListener("click",this.click)}ensureInView(){requestAnimationFrame(()=>this.scrollIntoView({block:"nearest"}))}click(){this.dispatchEvent(new CustomEvent("actionsSelected",{detail:this.action,bubbles:!0,composed:!0}))}updated(t){t.has("selected")&&this.selected&&this.ensureInView()}render(){let t,e;this.action.mdIcon?t=L`<mwc-icon part="ninja-icon" class="ninja-icon"
        >${this.action.mdIcon}</mwc-icon
      >`:this.action.icon&&(t=fe(this.action.icon||"")),this.action.hotkey&&(e=this.hotKeysJoinedView?this.action.hotkey.split(",").map(t=>{const e=t.split("+"),i=L`${function*(t,e){const i="function"==typeof e;if(void 0!==t){let n=-1;for(const s of t)n>-1&&(yield i?e(n):e),n++,yield s}}(e.map(t=>L`<kbd>${t}</kbd>`),"+")}`;return L`<div class="ninja-hotkey ninja-hotkeys">
            ${i}
          </div>`}):this.action.hotkey.split(",").map(t=>{const e=t.split("+").map(t=>L`<kbd class="ninja-hotkey">${t}</kbd>`);return L`<kbd class="ninja-hotkeys">${e}</kbd>`}));const i={selected:this.selected,"ninja-action":!0};return L`
      <div
        class="ninja-action"
        part="ninja-action ${this.selected?"ninja-selected":""}"
        class=${Kt(i)}
      >
        ${t}
        <div class="ninja-title">${this.action.title}</div>
        ${e}
      </div>
    `}};ki.styles=l`
    :host {
      display: flex;
      width: 100%;
    }
    .ninja-action {
      padding: 0.75em 1em;
      display: flex;
      border-left: 2px solid transparent;
      align-items: center;
      justify-content: start;
      outline: none;
      transition: color 0s ease 0s;
      width: 100%;
    }
    .ninja-action.selected {
      cursor: pointer;
      color: var(--ninja-selected-text-color);
      background-color: var(--ninja-selected-background);
      border-left: 2px solid var(--ninja-accent-color);
      outline: none;
    }
    .ninja-action.selected .ninja-icon {
      color: var(--ninja-selected-text-color);
    }
    .ninja-icon {
      font-size: var(--ninja-icon-size);
      max-width: var(--ninja-icon-size);
      max-height: var(--ninja-icon-size);
      margin-right: 1em;
      color: var(--ninja-icon-color);
      margin-right: 1em;
      position: relative;
    }

    .ninja-title {
      flex-shrink: 0.01;
      margin-right: 0.5em;
      flex-grow: 1;
      font-size: 0.8125em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .ninja-hotkeys {
      flex-shrink: 0;
      width: min-content;
      display: flex;
    }

    .ninja-hotkeys kbd {
      font-family: inherit;
    }
    .ninja-hotkey {
      background: var(--ninja-secondary-background-color);
      padding: 0.06em 0.25em;
      border-radius: var(--ninja-key-border-radius);
      text-transform: capitalize;
      color: var(--ninja-secondary-text-color);
      font-size: 0.75em;
      font-family: inherit;
    }

    .ninja-hotkey + .ninja-hotkey {
      margin-left: 0.5em;
    }
    .ninja-hotkeys + .ninja-hotkeys {
      margin-left: 1em;
    }
  `,wi([ht({type:Object})],ki.prototype,"action",void 0),wi([ht({type:Boolean})],ki.prototype,"selected",void 0),wi([ht({type:Boolean})],ki.prototype,"hotKeysJoinedView",void 0),ki=wi([lt("ninja-action")],ki);const xi=L` <div class="modal-footer" slot="footer">
  <span class="help">
    <svg
      version="1.0"
      class="ninja-examplekey"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 1280 1280"
    >
      <path
        d="M1013 376c0 73.4-.4 113.3-1.1 120.2a159.9 159.9 0 0 1-90.2 127.3c-20 9.6-36.7 14-59.2 15.5-7.1.5-121.9.9-255 1h-242l95.5-95.5 95.5-95.5-38.3-38.2-38.2-38.3-160 160c-88 88-160 160.4-160 161 0 .6 72 73 160 161l160 160 38.2-38.3 38.3-38.2-95.5-95.5-95.5-95.5h251.1c252.9 0 259.8-.1 281.4-3.6 72.1-11.8 136.9-54.1 178.5-116.4 8.6-12.9 22.6-40.5 28-55.4 4.4-12 10.7-36.1 13.1-50.6 1.6-9.6 1.8-21 2.1-132.8l.4-122.2H1013v110z"
      />
    </svg>

    to select
  </span>
  <span class="help">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey"
      viewBox="0 0 24 24"
    >
      <path d="M0 0h24v24H0V0z" fill="none" />
      <path
        d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"
      />
    </svg>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey"
      viewBox="0 0 24 24"
    >
      <path d="M0 0h24v24H0V0z" fill="none" />
      <path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z" />
    </svg>
    to navigate
  </span>
  <span class="help">
    <span class="ninja-examplekey esc">esc</span>
    to close
  </span>
  <span class="help">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey backspace"
      viewBox="0 0 20 20"
      fill="currentColor"
    >
      <path
        fill-rule="evenodd"
        d="M6.707 4.879A3 3 0 018.828 4H15a3 3 0 013 3v6a3 3 0 01-3 3H8.828a3 3 0 01-2.12-.879l-4.415-4.414a1 1 0 010-1.414l4.414-4.414zm4 2.414a1 1 0 00-1.414 1.414L10.586 10l-1.293 1.293a1 1 0 101.414 1.414L12 11.414l1.293 1.293a1 1 0 001.414-1.414L13.414 10l1.293-1.293a1 1 0 00-1.414-1.414L12 8.586l-1.293-1.293z"
        clip-rule="evenodd"
      />
    </svg>
    move to parent
  </span>
</div>`,Pi=l`
  :host {
    --ninja-width: 640px;
    --ninja-backdrop-filter: none;
    --ninja-overflow-background: rgba(255, 255, 255, 0.5);
    --ninja-text-color: rgb(60, 65, 73);
    --ninja-font-size: 16px;
    --ninja-top: 20%;

    --ninja-key-border-radius: 0.25em;
    --ninja-accent-color: rgb(110, 94, 210);
    --ninja-secondary-background-color: rgb(239, 241, 244);
    --ninja-secondary-text-color: rgb(107, 111, 118);

    --ninja-selected-background: rgb(248, 249, 251);

    --ninja-icon-color: var(--ninja-secondary-text-color);
    --ninja-icon-size: 1.2em;
    --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);

    --ninja-modal-background: #fff;
    --ninja-modal-shadow: rgb(0 0 0 / 50%) 0px 16px 70px;

    --ninja-actions-height: 300px;
    --ninja-group-text-color: rgb(144, 149, 157);

    --ninja-footer-background: rgba(242, 242, 242, 0.4);

    --ninja-placeholder-color: #8e8e8e;

    font-size: var(--ninja-font-size);

    --ninja-z-index: 1;
  }

  :host(.dark) {
    --ninja-backdrop-filter: none;
    --ninja-overflow-background: rgba(0, 0, 0, 0.7);
    --ninja-text-color: #7d7d7d;

    --ninja-modal-background: rgba(17, 17, 17, 0.85);
    --ninja-accent-color: rgb(110, 94, 210);
    --ninja-secondary-background-color: rgba(51, 51, 51, 0.44);
    --ninja-secondary-text-color: #888;

    --ninja-selected-text-color: #eaeaea;
    --ninja-selected-background: rgba(51, 51, 51, 0.44);

    --ninja-icon-color: var(--ninja-secondary-text-color);
    --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);

    --ninja-modal-shadow: 0 16px 70px rgba(0, 0, 0, 0.2);

    --ninja-group-text-color: rgb(144, 149, 157);

    --ninja-footer-background: rgba(30, 30, 30, 85%);
  }

  .modal {
    display: none;
    position: fixed;
    z-index: var(--ninja-z-index);
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background: var(--ninja-overflow-background);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-backdrop-filter: var(--ninja-backdrop-filter);
    backdrop-filter: var(--ninja-backdrop-filter);
    text-align: left;
    color: var(--ninja-text-color);
    font-family: var(--ninja-font-family);
  }
  .modal.visible {
    display: block;
  }

  .modal-content {
    position: relative;
    top: var(--ninja-top);
    margin: auto;
    padding: 0;
    display: flex;
    flex-direction: column;
    flex-shrink: 1;
    -webkit-box-flex: 1;
    flex-grow: 1;
    min-width: 0px;
    will-change: transform;
    background: var(--ninja-modal-background);
    border-radius: 0.5em;
    box-shadow: var(--ninja-modal-shadow);
    max-width: var(--ninja-width);
    overflow: hidden;
  }

  .bump {
    animation: zoom-in-zoom-out 0.2s ease;
  }

  @keyframes zoom-in-zoom-out {
    0% {
      transform: scale(0.99);
    }
    50% {
      transform: scale(1.01, 1.01);
    }
    100% {
      transform: scale(1, 1);
    }
  }

  .ninja-github {
    color: var(--ninja-keys-text-color);
    font-weight: normal;
    text-decoration: none;
  }

  .actions-list {
    max-height: var(--ninja-actions-height);
    overflow: auto;
    scroll-behavior: smooth;
    position: relative;
    margin: 0;
    padding: 0.5em 0;
    list-style: none;
    scroll-behavior: smooth;
  }

  .group-header {
    height: 1.375em;
    line-height: 1.375em;
    padding-left: 1.25em;
    padding-top: 0.5em;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    font-size: 0.75em;
    line-height: 1em;
    color: var(--ninja-group-text-color);
    margin: 1px 0;
  }

  .modal-footer {
    background: var(--ninja-footer-background);
    padding: 0.5em 1em;
    display: flex;
    /* font-size: 0.75em; */
    border-top: var(--ninja-separate-border);
    color: var(--ninja-secondary-text-color);
  }

  .modal-footer .help {
    display: flex;
    margin-right: 1em;
    align-items: center;
    font-size: 0.75em;
  }

  .ninja-examplekey {
    background: var(--ninja-secondary-background-color);
    padding: 0.06em 0.25em;
    border-radius: var(--ninja-key-border-radius);
    color: var(--ninja-secondary-text-color);
    width: 1em;
    height: 1em;
    margin-right: 0.5em;
    font-size: 1.25em;
    fill: currentColor;
  }
  .ninja-examplekey.esc {
    width: auto;
    height: auto;
    font-size: 1.1em;
  }
  .ninja-examplekey.backspace {
    opacity: 0.7;
  }
`;var ji=function(t,e,i,n){var s,o=arguments.length,r=o<3?e:null===n?n=Object.getOwnPropertyDescriptor(e,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,n);else for(var a=t.length-1;a>=0;a--)(s=t[a])&&(r=(o<3?s(r):o>3?s(e,i,r):s(e,i))||r);return o>3&&r&&Object.defineProperty(e,i,r),r};let Oi=class extends rt{constructor(){super(...arguments),this.placeholder="Type a command or search...",this.disableHotkeys=!1,this.hideBreadcrumbs=!1,this.openHotkey="cmd+k,ctrl+k",this.navigationUpHotkey="up,shift+tab",this.navigationDownHotkey="down,tab",this.closeHotkey="esc",this.goBackHotkey="backspace",this.selectHotkey="enter",this.hotKeysJoinedView=!1,this.noAutoLoadMdIcons=!1,this.data=[],this.visible=!1,this._bump=!0,this._actionMatches=[],this._search="",this._flatData=[],this._headerRef=Rt()}open(t={}){this._bump=!0,this.visible=!0,this._headerRef.value.focusSearch(),this._actionMatches.length>0&&(this._selected=this._actionMatches[0]),this.setParent(t.parent)}close(){this._bump=!1,this.visible=!1}setParent(t){this._currentRoot=t||void 0,this._selected=void 0,this._search="",this._headerRef.value.setSearch("")}get breadcrumbs(){var t;const e=[];let i=null===(t=this._selected)||void 0===t?void 0:t.parent;if(i)for(e.push(i);i;){const t=this._flatData.find(t=>t.id===i);(null==t?void 0:t.parent)&&e.push(t.parent),i=t?t.parent:void 0}return e.reverse()}connectedCallback(){super.connectedCallback(),this.noAutoLoadMdIcons||document.fonts.load("24px Material Icons","apps").then(()=>{}),this._registerInternalHotkeys()}disconnectedCallback(){super.disconnectedCallback(),this._unregisterInternalHotkeys()}_flattern(t,e){let i=[];return t||(t=[]),t.map(t=>{const n=t.children&&t.children.some(t=>"string"==typeof t),s={...t,parent:t.parent||e};return n||(s.children&&s.children.length&&(e=t.id,i=[...i,...s.children]),s.children=s.children?s.children.map(t=>t.id):[]),s}).concat(i.length?this._flattern(i,e):i)}update(t){t.has("data")&&!this.disableHotkeys&&(this._flatData=this._flattern(this.data),this._flatData.filter(t=>!!t.hotkey).forEach(t=>{de(t.hotkey,e=>{e.preventDefault(),t.handler&&t.handler(t)})})),super.update(t)}_registerInternalHotkeys(){this.openHotkey&&de(this.openHotkey,t=>{t.preventDefault(),this.visible?this.close():this.open()}),this.selectHotkey&&de(this.selectHotkey,t=>{this.visible&&(t.preventDefault(),this._actionSelected(this._actionMatches[this._selectedIndex]))}),this.goBackHotkey&&de(this.goBackHotkey,t=>{this.visible&&(this._search||(t.preventDefault(),this._goBack()))}),this.navigationDownHotkey&&de(this.navigationDownHotkey,t=>{this.visible&&(t.preventDefault(),this._selectedIndex>=this._actionMatches.length-1?this._selected=this._actionMatches[0]:this._selected=this._actionMatches[this._selectedIndex+1])}),this.navigationUpHotkey&&de(this.navigationUpHotkey,t=>{this.visible&&(t.preventDefault(),0===this._selectedIndex?this._selected=this._actionMatches[this._actionMatches.length-1]:this._selected=this._actionMatches[this._selectedIndex-1])}),this.closeHotkey&&de(this.closeHotkey,()=>{this.visible&&this.close()})}_unregisterInternalHotkeys(){this.openHotkey&&de.unbind(this.openHotkey),this.selectHotkey&&de.unbind(this.selectHotkey),this.goBackHotkey&&de.unbind(this.goBackHotkey),this.navigationDownHotkey&&de.unbind(this.navigationDownHotkey),this.navigationUpHotkey&&de.unbind(this.navigationUpHotkey),this.closeHotkey&&de.unbind(this.closeHotkey)}_actionFocused(t,e){this._selected=t,e.target.ensureInView()}_onTransitionEnd(){this._bump=!1}_goBack(){const t=this.breadcrumbs.length>1?this.breadcrumbs[this.breadcrumbs.length-2]:void 0;this.setParent(t)}render(){const t={bump:this._bump,"modal-content":!0},e={visible:this.visible,modal:!0},i=this._flatData.filter(t=>{var e;const i=new RegExp(this._search,"gi"),n=t.title.match(i)||(null===(e=t.keywords)||void 0===e?void 0:e.match(i));return(!this._currentRoot&&this._search||t.parent===this._currentRoot)&&n}).reduce((t,e)=>t.set(e.section,[...t.get(e.section)||[],e]),new Map);this._actionMatches=[...i.values()].flat(),this._actionMatches.length>0&&-1===this._selectedIndex&&(this._selected=this._actionMatches[0]),0===this._actionMatches.length&&(this._selected=void 0);const n=t=>L` ${jt(t,t=>t.id,t=>{var e;return L`<ninja-action
            exportparts="ninja-action,ninja-selected,ninja-icon"
            .selected=${Ot(t.id===(null===(e=this._selected)||void 0===e?void 0:e.id))}
            .hotKeysJoinedView=${this.hotKeysJoinedView}
            @mouseover=${e=>this._actionFocused(t,e)}
            @actionsSelected=${t=>this._actionSelected(t.detail)}
            .action=${t}
          ></ninja-action>`})}`,s=[];return i.forEach((t,e)=>{const i=e?L`<div class="group-header">${e}</div>`:void 0;s.push(L`${i}${n(t)}`)}),L`
      <div @click=${this._overlayClick} class=${Kt(e)}>
        <div class=${Kt(t)} @animationend=${this._onTransitionEnd}>
          <ninja-header
            exportparts="ninja-input,ninja-input-wrapper"
            ${It(this._headerRef)}
            .placeholder=${this.placeholder}
            .hideBreadcrumbs=${this.hideBreadcrumbs}
            .breadcrumbs=${this.breadcrumbs}
            @change=${this._handleInput}
            @setParent=${t=>this.setParent(t.detail.parent)}
            @close=${this.close}
          >
          </ninja-header>
          <div class="modal-body">
            <div class="actions-list" part="actions-list">${s}</div>
          </div>
          <slot name="footer"> ${xi} </slot>
        </div>
      </div>
    `}get _selectedIndex(){return this._selected?this._actionMatches.indexOf(this._selected):-1}_actionSelected(t){var e;if(this.dispatchEvent(new CustomEvent("selected",{detail:{search:this._search,action:t},bubbles:!0,composed:!0})),t){if(t.children&&(null===(e=t.children)||void 0===e?void 0:e.length)>0&&(this._currentRoot=t.id,this._search=""),this._headerRef.value.setSearch(""),this._headerRef.value.focusSearch(),t.handler){const e=t.handler(t);(null==e?void 0:e.keepOpen)||this.close()}this._bump=!0}}async _handleInput(t){this._search=t.detail.search,await this.updateComplete,this.dispatchEvent(new CustomEvent("change",{detail:{search:this._search,actions:this._actionMatches},bubbles:!0,composed:!0}))}_overlayClick(t){var e;(null===(e=t.target)||void 0===e?void 0:e.classList.contains("modal"))&&this.close()}};Oi.styles=[Pi],ji([ht({type:String})],Oi.prototype,"placeholder",void 0),ji([ht({type:Boolean})],Oi.prototype,"disableHotkeys",void 0),ji([ht({type:Boolean})],Oi.prototype,"hideBreadcrumbs",void 0),ji([ht()],Oi.prototype,"openHotkey",void 0),ji([ht()],Oi.prototype,"navigationUpHotkey",void 0),ji([ht()],Oi.prototype,"navigationDownHotkey",void 0),ji([ht()],Oi.prototype,"closeHotkey",void 0),ji([ht()],Oi.prototype,"goBackHotkey",void 0),ji([ht()],Oi.prototype,"selectHotkey",void 0),ji([ht({type:Boolean})],Oi.prototype,"hotKeysJoinedView",void 0),ji([ht({type:Boolean})],Oi.prototype,"noAutoLoadMdIcons",void 0),ji([ht({type:Array,hasChanged:()=>!0})],Oi.prototype,"data",void 0),ji([dt()],Oi.prototype,"visible",void 0),ji([dt()],Oi.prototype,"_bump",void 0),ji([dt()],Oi.prototype,"_actionMatches",void 0),ji([dt()],Oi.prototype,"_search",void 0),ji([dt()],Oi.prototype,"_currentRoot",void 0),ji([dt()],Oi.prototype,"_flatData",void 0),ji([dt()],Oi.prototype,"breadcrumbs",null),ji([dt()],Oi.prototype,"_selected",void 0),Oi=ji([lt("ninja-keys")],Oi)}}]);
//# sourceMappingURL=async-feffery_shortcut_panel.js.map
//# sourceMappingURL=async-feffery_shortcut_panel.js.map
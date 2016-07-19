/**
 * 小ネタ集.
 */

import * as Types from './Types';


/**
 * Formとthis.stateの同期.
 *
 * @see https://facebook.github.io/react/docs/two-way-binding-helpers.html
 */
export function valueLink(component: any, ...path: string[]): Types.TValueLink {
  let lastKey = path.pop();
  let dig = () => path.reduce((prev, current, index, array) => prev[current], component.state);

  // 間違い防止の為、チェックする.
  // compile-timeでチェックできないから...
  if (!(lastKey in dig())) {
    alert('バグ発見です。\n\n' +
      'function valueLink(component: any, ...path: string[]): Types.TValueLink\n' +
      'component: ' + component + '\n' +
      'path: ' + path);
  }

  let callback = (newValue) => {
    dig()[lastKey] = newValue;
    component.setState(component.state);
  };

  return {
    value: dig()[lastKey],
    requestChange: callback
  };
}

/**
 * <input type='checkbox' onChange={ onChangeLink(obj, 'root', '...', 'leaf') } >
 */
export function onCheckedLink(component: any, ...path: string[]): (Event) => void {
  let lastKey = path.pop();
  let dig = () => path.reduce((prev, current, index, array) => prev[current], component.state);

  // 間違い防止の為、チェックする.
  // compile-timeでチェックできないから...
  if (!(lastKey in dig())) {
    alert('バグ発見です。\n\n' +
      'function valueLink(component: any, ...path: string[]): Types.TValueLink\n' +
      'component: ' + component + '\n' +
      'path: ' + path);
  }

  let f = (e) => {
    dig()[lastKey] = e.target.checked;
    component.setState(component.state);
  };

  return f;
}

/**
 * オブジェクトの '_' で始まるメソッドをbind(this)します。
 *
 * @param {any} obj
 */
export function bindPrivateMethods(obj) {
  for (name in obj) {
    // is this function ?
    if (typeof obj[name] !== 'function') {
      continue;
    }

    // treats function startswith '_' as private.
    if (name.indexOf('_') !== 0) {
      continue;
    }

    // bind.
    obj[name] = obj[name].bind(obj);
  }
};

/**
 * @return true if session exists.
 */
export function hasSession(): boolean {
  return getCookie('session') !== null;
}

/**
 * @return session if exists.
 */
export function getSession(): Types.TSession {
  if (!hasSession()) {
    return null;
  }

  // flaskのSecure sessionで中身が見れないので、Clietnでも独自管理.
  // (やり方はあるけど、Secureじゃなくなるし...)
  let session: Types.TSession = { userId: getCookie('userId') };
  return session;
}

/**
 * @see http://memo.ark-under.net/memo/404
 */
export function getCookie(c_name: string): string {
  if (document.cookie.length <= 0) {
    return null;
  }

  let st = document.cookie.indexOf(c_name + '=');
  if (st === -1) {
    return null;
  }

  st = st + c_name.length + 1;
  let ed = document.cookie.indexOf(';', st);
  ed = (ed === -1) ? document.cookie.length : ed;

  return decodeURI(document.cookie.substring(st, ed));
}

/**
 * @see http://memo.ark-under.net/memo/404
 */
export function setCookie(c_name: string, value: string, expiredays = 365): void {
  // pathの指定
  let path = location.pathname;

  // pathをフォルダ毎に指定する場合のIE対策
  let paths = new Array();
  paths = path.split('/');
  if (paths[paths.length - 1] !== '') {
    paths[paths.length - 1] = '';
    path = paths.join('/');
  }

  // 有効期限の日付
  let extime = new Date().getTime();
  let cltime = new Date(extime + (60 * 60 * 24 * 1000 * expiredays));
  let exdate = cltime.toUTCString();

  // クッキーに保存する文字列を生成
  let s = '';
  s += c_name + '=' + encodeURIComponent(value); // 値はエンコードしておく
  s += '; path=' + path;
  if (expiredays) {
    s += '; expires=' + exdate + '; ';
  } else {
    s += '; ';
  }

  // クッキーに保存
  document.cookie = s;
}

/**
 * URLを正規化 (protocolを外す、"/"をtirmする) して返す.
 */
export function normalizeUrl(url: string) {
  return url.replace('https://', '').replace('http://', '').replace(/\/$/, '');
}

/**
 * HTTPS URL ("https://""を付ける、"/"をtirmする) にして返す.
 */
export function httpUrl(url: string) {
  let cleaned = normalizeUrl(url);
  return [ 'http://', cleaned ].join('');
}

/**
 * HTTPS URL ("https://""を付ける、"/"をtirmする) にして返す.
 */
export function httpsUrl(url: string) {
  let cleaned = normalizeUrl(url);
  return [ 'https://', cleaned ].join('');
}

/**
 * @return true/false.
 */
export function isUrl(url: string) {
  let regexes = [ /\.com$/, /\.jp$/ ];
  let ret = regexes.reduce((pre, cur) => pre ? pre : cur.test(url), false);
  return ret;
}

export function b64EncodeUnicode(str) {
  return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
    return String.fromCharCode(parseInt('0x' + p1, 16));
  }));
}

export function b64DecodeUnicode(str) {
  return decodeURIComponent(Array.prototype.map.call(atob(str), function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
}

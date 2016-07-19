/*
 * URLハッシュを監視して、Page?に通知する.
 */

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as crossroads from 'crossroads';
import * as hasher from 'hasher';
import * as Constants from './Constants';

import { hasSession } from './Utils';


export function startRouting() {
  // index.
  //crossroads.addRoute('', () => _sessionRequired(<Index />));

  // routed.
  crossroads.routed.add(request => {
    console.log('Valid Path: ' + request);
  });

  // bypassed.
  crossroads.bypassed.add(request => {
    console.log('404 Not Found: ' + request);
    //_publicPage(<P404 />);
  });

  // setup hasher
  hasher.initialized.add(_parseHash);
  hasher.changed.add(_parseHash);
  hasher.init();
}

function _parseHash(newHash, oldHash) {
  crossroads.parse(newHash);
}

function _publicPage(elm): void {
  ReactDOM.render(
    elm,
    document.getElementById('react-content')
  );
}

function _sessionRequired(elm): void {
  // session無かったら、ログインページへ.
  if (!hasSession()) {
    return hasher.setHash('login');
  }

  ReactDOM.render(
    elm,
    document.getElementById('react-content')
  );
}

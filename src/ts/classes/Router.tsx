/*
 * URLハッシュを監視して、Page?に通知する.
 */

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as crossroads from 'crossroads';
import * as hasher from 'hasher';

import { hasSession } from './Utils';
import { EstimatedCharge } from '../EstimatedCharge';
import { Monthly } from '../Monthly';


export function startRouting() {
  // pages.
  crossroads.addRoute('', () => _publicPage(<EstimatedCharge />));
  crossroads.addRoute('/estimated_charge', () => _publicPage(<EstimatedCharge />));
  crossroads.addRoute('/monthly', () => _publicPage(<Monthly />));

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

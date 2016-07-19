/*****************************
AppStore
******************************/

import { AbstractStore } from './AbstractStore';
import { TPayload, TAction } from '../FluxDispatcher';
import * as FluxConstants from '../FluxConstants';


const _CHANGE_EVENT = 'change-app-store';

export class AppStore extends AbstractStore {

  private static _instance: AppStore = null;

  private _docs: { [key: string]: any };

  public static getInstance(): AppStore {
    if (AppStore._instance === null) {
      AppStore._instance = new AppStore();
    }
    return AppStore._instance;
  }

  constructor() {
    if (AppStore._instance) {
      throw new Error('must use the getInstance.');
    }
    super(_CHANGE_EVENT);
    this._docs = {};
    AppStore._instance = this;
  }

  getDoc(docId: string) {
    if (docId in this._docs) {
      return this._docs[docId];
    }

    return null;
  }

  protected _dispatcher(payload: TPayload): void {
    let ActionTypes = FluxConstants.ActionTypes;
    let action: TAction = payload.action;

    switch (action.type) {
      case ActionTypes.FETCH_USERDOC:
        // must be there...
        let docId = action['docId'];
        let data = action['data'];

        // store it.
        this._docs[docId] = data;

        this.emitChange();
        break;
    }
  }
}

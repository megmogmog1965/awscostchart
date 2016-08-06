/*****************************
AbstractStore
******************************/

import { EventEmitter } from 'events';

import { FluxDispatcher, TPayload } from '../FluxDispatcher';


export class AbstractStore extends EventEmitter {

  private _storeId: string;
  private _dispatchToken: string;

  constructor(storeId: string) {
    super();
    this._storeId = storeId;
    this._dispatchToken = this._registerDispatcher();
  }

  emitChange(): void {
    this.emit(this._storeId);
  }

  addChangeListener(callback): void {
    this.on(this._storeId, callback);
  }

  removeChangeListener(callback): void {
    this.removeListener(this._storeId, callback);
  }

  /**
   * サブクラスでdispatcherの登録を行う.
   *
   * @return callback for dispatcher.
   */
  protected _dispatcher(payload: TPayload): void {
    throw new Error('Not implemented yet: AbstractStore._dispatcher');
  }

  private _registerDispatcher(): string {
    // create callback.
    let callback: (payload: TPayload) => void = this._dispatcher.bind(this);

    // register it.
    return FluxDispatcher.getInstance().register(callback);
  }
}

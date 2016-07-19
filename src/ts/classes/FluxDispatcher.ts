/*****************************
FluxDispatcher

Flux:
 - XXXStoreが dispatcher.register((payload: TPayload) => void) でcallbackを登録.
 - Component(view)が XXXActionsの任意のメソッドを呼ぶ.
 - XXXActionsが dispatcher.handleViewAction({action: any, ... }) を呼ぶ.
 - Dispatcherが 登録済みのXXXStoreの callback を呼ぶ.

@see https://facebook.github.io/flux/docs/todo-list.html
@see http://qiita.com/koba04/items/b32ba449d753fdb2b597
******************************/

import { Dispatcher } from 'flux';
import * as FluxConstants from './FluxConstants';


export interface TAction {
  type: FluxConstants.ActionTypes;
  [id: string]: any;
}

export interface TPayload {
  source: number;
  action: TAction;
}

export class FluxDispatcher extends Dispatcher<TPayload> {

  private static _instance: FluxDispatcher = null;

  public static getInstance(): FluxDispatcher {
    if (FluxDispatcher._instance === null) {
      FluxDispatcher._instance = new FluxDispatcher();
    }
    return FluxDispatcher._instance;
  }

  constructor() {
    if (FluxDispatcher._instance) {
      throw new Error('must use the getInstance.');
    }
    super();
    FluxDispatcher._instance = this;
  }

  /**
   * XXXActionsから呼ばれる.
   *
   * @param { action: any, ... } action
   */
  handleViewAction(action: TAction): void {
    this.dispatch({
      source: FluxConstants.PayloadSources.VIEW_ACTION,
      action: action
    });
  }
}

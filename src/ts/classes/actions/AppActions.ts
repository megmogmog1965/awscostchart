/*****************************
AppActions
******************************/

import { FluxDispatcher } from '../FluxDispatcher';
import { ActionTypes } from '../FluxConstants';


export class AppActions {

  /**
   * @param {string} docId
   */
  static fetchDoc(docId: string): void {
    // login.
    $.ajax({
      type: 'GET',
      url: '/apis/docs/' + docId,
      dataType: 'json'
    }).pipe(
      res => {
        // dispatch.
        FluxDispatcher.getInstance().handleViewAction({
          type: ActionTypes.FETCH_USERDOC,
          docId: docId,
          data: res
        });
      },
      res => {
        console.log(res);
      }
    );
  }
};

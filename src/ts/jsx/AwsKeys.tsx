import * as React from 'react';
import { Promise } from 'es6-promise';
import * as $ from 'jquery';

import * as Types from '../classes/Types';
import { bindPrivateMethods } from '../classes/Utils';
import { Header } from './Header';
import { StackedColumnChart } from './StackedColumnChart';


export interface State {
  awskeys: Types.TAwsCredential[];
}

export interface Props {}

export class AwsKeys extends React.Component<Props, State> {

  constructor() {
    super();
    bindPrivateMethods(this);
  }

  componentWillMount() {
    this.state = { awskeys: [] };
  }

  componentDidMount() {
    this._draw_table();
  }

  componentWillReceiveProps(nextProps: Props) {
    this._draw_table();
  }

  private _draw_table(): void {
    let p1 = new Promise((resolve, reject) => {
      $.ajax({
      url: '/apis/awskeys',
      dataType: 'json'
      })
      .done((awskeys: { awskeys: Types.TAwsCredential[] }) => {
        resolve(awskeys.awskeys);
      })
      .fail((reason) => {
        reject(reason);
      });
    });

    Promise.all([ p1 ]).then(
      (data: any[]) => {
        this.state.awskeys = data[0];
        this.setState(this.state);
      },
      (reason) => {
        alert('error: ' + reason);
      }
    );
  }

  render () {
    return (
      <div className='AwsKeys'>
        <Header />
        <div className='content'>
          <h1>Registered AWS Keys</h1>

          <table className='pure-table'>
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Access Key ID</th>
              </tr>
            </thead>
            <tbody>
            {
              this.state.awskeys.map((key, index) =>
              <tr>
                <td>{ index + 1 }</td>
                <td>{ key.name }</td>
                <td>{ key.aws_access_key_id }</td>
              </tr>)
            }
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

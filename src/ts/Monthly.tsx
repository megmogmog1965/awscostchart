import * as React from 'react';
import { Promise } from 'es6-promise';
import * as $ from 'jquery';

import * as Types from './classes/Types';
import { bindPrivateMethods } from './classes/Utils';
import { Header } from './Header';
import { StackedColumnChart } from './StackedColumnChart';


export interface State {
  monthlyCharges: TCharges;
  awskeys: Types.TAwsCredential[];
}

export interface Props {}

interface TCharges {
  [accesskeyid: string]: Types.TEstimatedCharge;
}

export class Monthly extends React.Component<Props, State> {

  constructor() {
    super();
    bindPrivateMethods(this);
  }

  componentWillMount() {
    this.state = { monthlyCharges: {}, awskeys: [] };
  }

  componentDidMount() {
    this._draw_chart();
  }

  componentWillReceiveProps(nextProps: Props) {
    this._draw_chart();
  }

  private _draw_chart(): void {
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

    let p2 = new Promise((resolve, reject) => {
      $.ajax({
      url: '/apis/monthly',
      dataType: 'json'
      })
      .done((charges: TCharges) => {
        resolve(charges);
      })
      .fail((reason) => {
        reject(reason);
      });
    });

    Promise.all([ p1, p2 ]).then(
      (data: any[]) => {
        this.state.awskeys = data[0];
        this.state.monthlyCharges = data[1];
        this.setState(this.state);
      },
      (reason) => {
        alert('error: ' + reason);
      }
    );
  }

  render () {
    return (
      <div className='Monthly'>
        <Header />
        <div className='content'>
          <h1>Monthly Costs</h1>
          {
            this.state.awskeys.map((key) => <StackedColumnChart title={ key.name }
            estimatedCharge={ this.state.monthlyCharges[key.aws_access_key_id] } />)
          }
        </div>
      </div>
    );
  }
}

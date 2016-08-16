import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as Highcharts from 'highcharts';
import * as $ from 'jquery';

import * as Types from './classes/Types';
import { bindPrivateMethods } from './classes/Utils';


export interface State {}

export interface Props {
  title: string;
  estimatedCharge: Types.TEstimatedCharge;
}

export class StackedColumnChart extends React.Component<Props, State> {

  private _id: string = 'StackedColumnChart_' + Math.random();

  constructor() {
    super();
    bindPrivateMethods(this);
  }

  componentDidMount() {
    this._draw_chart();
  }

  componentWillReceiveProps(nextProps: Props) {
    this._draw_chart();
  }

  private _draw_chart(): void {
    let converted = Object.keys(this.props.estimatedCharge).reduce(
      (pre, cur) => $.extend(true, {}, pre,
        { [cur]: this.props.estimatedCharge[cur].map((p: Types.TChargeSample) => [ p.timestamp, p.value ]) }),
      {}
    );

    this._render_highcharts(converted);
  }

  /**
   * @param data: [ [ unixtime, value ], ... ]
   */
  private _render_highcharts(data): void {
    let elmId = 'stackedcolumnchartelm_' + this._id;
    let element = React.createElement('div', { id: elmId });
    ReactDOM.render(element, document.getElementById(this._id), () => {
      // addFunnel(Highcharts);
      Highcharts.chart(elmId, {
        chart: {
            type: 'column'
        },
        title: {
            text: this.props.title
        },
        // subtitle: {
        //     text: 'Shows AWS estimated charges for each service.'
        // },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%e. %b',
                week: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'USD'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b, %Y}: {point.y:.0f} USD'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    // color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                    color: 'white',
                    style: {
                        textShadow: '0 0 3px black'
                    }
                }
            }
        },
        series: [
            { name: 'AWSDataTransfer', data: data.AWSDataTransfer },
            { name: 'AWSQueueService', data: data.AWSQueueService },
            { name: 'AmazonEC2', data: data.AmazonEC2 },
            { name: 'AmazonES', data: data.AmazonES },
            { name: 'AmazonElastiCache', data: data.AmazonElastiCache },
            { name: 'AmazonRDS', data: data.AmazonRDS },
            { name: 'AmazonRoute53', data: data.AmazonRoute53 },
            { name: 'AmazonS3', data: data.AmazonS3 },
            { name: 'AmazonSNS', data: data.AmazonSNS },
            { name: 'awskms', data: data.awskms }
        ]
      });
    });
  }

  render () {
    return (
      <div className='StackedColumnChart chart'>
        <div id={ this._id } style={ { width: '100%' } }></div>
      </div>
    );
  }
}

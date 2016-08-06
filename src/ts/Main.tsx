import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as Highcharts from 'highcharts';


export interface State {}

export interface Props {}

interface Point {
  timestamp: number;
  value: number;
  aws_access_key_id: string;
}

interface Costs {
  AWSDataTransfer: Point[];
  AWSQueueService: Point[];
  AmazonEC2: Point[];
  AmazonES: Point[];
  AmazonElastiCache: Point[];
  AmazonRDS: Point[];
  AmazonRoute53: Point[];
  AmazonS3: Point[];
  AmazonSNS: Point[];
  awskms: Point[];
}

export class Main extends React.Component<Props, State> {

  constructor() {
    super();

    // @fixme: bind.
    this._draw_chart = this._draw_chart.bind(this);
    this._render_highcharts = this._render_highcharts.bind(this);
  }

  componentDidMount() {
    this._draw_chart();
  }

  componentWillReceiveProps(nextProps: Props) {
    this._draw_chart();
  }

  private _draw_chart(): void {
    $.ajax({
      url: '/apis/estimated_charge',
      dataType: 'json'
    })
    .done((costs: { accesskeyid: Costs }) => {
      let converted = Object.keys(costs.accesskeyid).reduce(
        (pre, cur) => $.extend(true, {}, pre, { [cur]: costs.accesskeyid[cur].map((p: Point) => [ p.timestamp, p.value ]) }),
        {}
      );
      this._render_highcharts(converted);
    })
    .fail((data) => {
      alert('error: ' + data);
    });
  }

  /**
   * @param data: [ [ unixtime, value ], ... ]
   */
  private _render_highcharts(data): void {
    let element = React.createElement('div', { id: 'chart' });
    ReactDOM.render(element, document.getElementById('container'), function () {
      // addFunnel(Highcharts);
      Highcharts.chart('chart', {
        chart: {
            // type: 'spline'
            type: 'area'
        },
        title: {
            text: 'AWS Cost Chart'
        },
        subtitle: {
            text: 'Shows AWS estimated charges for each service.'
        },
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
            // spline: {
            //     marker: {
            //         enabled: false
            //     }
            // }
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    enabled: false
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
      <div className='Main'>
        <div id='container' style={ { width: '100%' } }></div>
      </div>
    );
  }
}

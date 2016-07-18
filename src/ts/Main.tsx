import * as React from 'react';


declare var $: any;
declare var Highcharts: any;


export interface State {}

export interface Props {}

export class Main extends React.Component<Props, State> {

  constructor () {
    super();
  }

  componentDidMount() {
    this._render_by_jquery();
  }

  componentDidUpdate() {
    this._render_by_jquery();
  }

  private _render_by_jquery() {
    // var chart1; // globally available
    // $(function() {
    //       chart1 = new Highcharts.StockChart({
    //          chart: {
    //             renderTo: 'container'
    //          },
    //          rangeSelector: {
    //             selected: 1
    //          },
    //          series: [{
    //             name: 'USD to EUR',
    //             data: usdtoeur // predefined JavaScript array
    //          }]
    //       });
    //    });

    $(function () {
      $('#container').highcharts({
        chart: {
          type: 'bar'
        },
        title: {
          text: 'Fruit Consumption'
        },
        xAxis: {
          categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
          title: {
            text: 'Fruit eaten'
          }
        },
        series: [{
          name: 'Jane',
          data: [1, 0, 4]
        }, {
          name: 'John',
          data: [5, 7, 3]
        }]
      });
    });
  }

  render () {
    return (
      <div className='Main'>
        <div id="container" style={ { width: '100%', height: '400px' } }></div>
      </div>
    );
  }
}

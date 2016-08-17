import * as React from 'react';

import { bindPrivateMethods } from './classes/Utils';


export interface State {}

export interface Props {}

export class Header extends React.Component<Props, State> {

  constructor() {
    super();
    bindPrivateMethods(this);
  }

  componentWillMount() {
    this.state = {};
  }

  componentDidMount() {
    // nothing to be done.
  }

  componentWillReceiveProps(nextProps: Props) {
    // nothing to be done.
  }

  render () {
    return (
      <div className='Header'>
        <div className='left-align'>
          <div className='v-align-middle'>
            <div className='dropdown'>
              <div className='dropbtn'>
                <i className='fa fa-list' aria-hidden='true'></i>
                <span>Menu</span>
              </div>
              <div className='dropdown-content'>
                <a href='#/estimated_charge'>Estimated Charge</a>
                <a href='#/monthly'>Monthly Costs</a>
              </div>
            </div>
          </div>
        </div>

        <div className='right-align'>
          <div className='v-align-middle'>
            <a href='https://github.com/megmogmog1965/awscostchart' >
              <i className='fa fa-github fa-lg' aria-hidden='true'></i>
            </a>
          </div>
        </div>
      </div>
    );
  }
}

import React, { Component } from 'react';
import { render } from 'react-dom';
import { throttle, debounce } from 'throttle-debounce';
import Input from '@material-ui/core/Input';
import Table from './Table';

class Searchable extends Component {
  token = null;

  // state = {
  //   query: '',
  //   genes: [],
  // };

  constructor() {
    super();
    this.searchDebounced = debounce(500, this.search);
    this.searchThrottled = throttle(500, this.search);
  }

  componentDidMount() {
    this.search('');
  }

  search = query => {
    const url = `http://localhost:3000/variants?gene=like.${query}*&limit=15`;
    const token = {};
    this.token = token;

    fetch(url)
      .then(results => results.json())
      .then(data => {
        if (this.token === token && query.length > 1) {
          // this.setState({ data });
          { data };
        }
      });
  };

  onChange = e => {
    const { value } = e.target;
    this.setState(
      {
        value,
      },
      () => {
        if (value.length < 5) {
          this.searchThrottled(value);
        } else {
          this.searchDebounced(value);
        }
      }
    );
  };

  render() {
    return (
      <div id="searchable">
        <div id="search-input">
          <Input
            id="component-filled"
            fullWidth
            onChange={this.onChange}
            placeholder="Search for a gene name..."
          />
        </div>
        <div id="table-results">
          <Table
            data={this.props.data}
            header={[
              {
                name: 'Gene',
                prop: 'gene',
              },
              {
                name: 'Protein Change',
                prop: 'protein_change',
              },
              {
                name: 'Reported Classification',
                prop: 'reported_classification',
              },
              {
                name: 'ClinVar URL',
                prop: 'url',
              },
            ]}
          />
        </div>
      </div>
    );
  }
}

export default Searchable;
const wrapper = document.getElementById('searchable');
wrapper ? render(<Searchable />, wrapper) : false;

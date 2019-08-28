import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
  },
  paper: {
    marginTop: theme.spacing(3),
    width: '100%',
    overflowX: 'auto',
    marginBottom: theme.spacing(2),
  },
  table: {
    minWidth: 650,
  },
}));

const row = (x, i, header) => (
  <TableRow key={`tr-${i}`}>
    {header.map((y, k) => (
      <TableCell align="right" key={`trc-${k}`}>
        {x[y.prop]}
      </TableCell>
    ))}
  </TableRow>
);

export default ({ data, header }) => {
  return (
    <Table className={useStyles().table} size="small">
      <TableHead>
        <TableRow>
          {header.map((x, i) => (
            <TableCell key={`thc-${i}`} align="right">
              {x.name}
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>{data.map((x, i) => row(x, i, header))}</TableBody>
    </Table>
  );
};

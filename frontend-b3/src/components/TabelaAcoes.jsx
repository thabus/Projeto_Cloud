import { useState, useEffect } from 'react';
import {
  TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Box, TablePagination
} from "@mui/material";

function TabelaAcoes({ onFiltro, filtro, setFiltro, dados }) {
  
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // 1. ESTADO LOCAL: Guarda o que você digita instantaneamente sem travar
  const [termoBusca, setTermoBusca] = useState(filtro.ativo);

  useEffect(() => {
    setPage(0);
  }, [dados]);

  // 2. DEBOUNCE (A MÁGICA): Só aplica o filtro 500ms depois que você para de digitar
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      // Só atualiza o pai se o valor tiver mudado
      if (termoBusca !== filtro.ativo) {
         setFiltro(prev => ({ ...prev, ativo: termoBusca }));
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [termoBusca, setFiltro, filtro.ativo]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const formatarMoeda = (valor) => {
    if (!valor || valor === 0 || valor === "0" || valor === "None") return "-";
    return `R$ ${parseFloat(valor).toFixed(2)}`;
  };

  const calcularPrecoMedio = (row) => {
    const min = parseFloat(row.min_price);
    const max = parseFloat(row.max_price);
    const close = parseFloat(row.close_price);
    if (!min || !max || !close) return "-";
    const media = (min + max + close) / 3;
    return `R$ ${media.toFixed(2)}`;
  };

  return (
    <Box sx={{ width: "100%" }}> 
      <form
        style={{ display: "flex", gap: 12, marginBottom: 18, flexWrap: 'wrap' }}
        onSubmit={e => { e.preventDefault(); }}>
        <TextField
          label="Buscar ativo"
          // 3. Agora o input obedece ao estado local (rápido)
          value={termoBusca}
          onChange={e => setTermoBusca(e.target.value)}
          size="small"
        />
        <TextField
          label="De"
          type="date"
          size="small"
          value={filtro.de}
          onChange={e => setFiltro({ ...filtro, de: e.target.value })}
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="Até"
          type="date"
          size="small"
          value={filtro.ate}
          onChange={e => setFiltro({ ...filtro, ate: e.target.value })}
          InputLabelProps={{ shrink: true }}
        />
      </form>

      <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Ticker</strong></TableCell>
              <TableCell>Data</TableCell>
              <TableCell>Abertura</TableCell>
              <TableCell>Fechamento</TableCell>
              <TableCell><strong>Preço Médio (Est.)</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dados
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, idx) => (
                <TableRow key={idx} hover>
                  <TableCell><strong>{row.ticker}</strong></TableCell>
                  <TableCell>{row.trade_date}</TableCell>
                  <TableCell>{formatarMoeda(row.open_price || row.min_price)}</TableCell> 
                  <TableCell sx={{ color: row.close_price ? '#2566cf' : 'inherit', fontWeight: 'bold' }}>
                    {formatarMoeda(row.close_price)}
                  </TableCell>
                  <TableCell>{calcularPrecoMedio(row)}</TableCell>
                </TableRow>
            ))}
            {dados.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 3 }}>
                  Nenhum dado encontrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[10, 25, 50, 100]}
          component="div"
          count={dados.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Linhas:"
        />
      </TableContainer>
    </Box>
  );
}

export default TabelaAcoes;
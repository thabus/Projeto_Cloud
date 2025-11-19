import {
  TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Box
} from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

function TabelaAcoes({ onFiltro, filtro, setFiltro, dados }) {
  return (
    <Box sx={{ width: 500 }}>
      <form
        style={{ display: "flex", gap: 12, marginBottom: 18 }}
        onSubmit={e => { e.preventDefault(); onFiltro(); }}>
        <TextField
          label="Buscar ativo"
          value={filtro.ativo}
          onChange={e => setFiltro({ ...filtro, ativo: e.target.value })}
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
        <Button type="submit" variant="contained" sx={{ height: 40, bgcolor: "#2566cf" }}>
          FILTRAR
        </Button>
      </form>
      <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Data</TableCell>
              <TableCell>Abertura</TableCell>
              <TableCell>Fechamento</TableCell>
              <TableCell>Volume</TableCell>
              <TableCell>Preço Médio</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dados.map((row, idx) => (
              <TableRow key={idx}>
                <TableCell>{row.ticker}</TableCell>
                <TableCell>{row.trade_date}</TableCell>
                <TableCell>{row.min_price}</TableCell>
                <TableCell>{row.close_price}</TableCell>
                <TableCell>{row.volume || "--"}</TableCell>
                <TableCell>{row.preco_medio || "--"}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default TabelaAcoes;

app.post('/api/mentorias-inscritas', async (req, res) => {
  const { token } = req.body;

  // Substitua com a lógica de banco de dados real
  const mentorias = await db.query(
    'SELECT titulo, mentor, descricao, data FROM mentorias_inscritas WHERE token = $1',
    [token]
  );

  res.json(mentorias.rows);
});
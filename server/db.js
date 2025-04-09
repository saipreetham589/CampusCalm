const sql = require('mssql');
require('dotenv').config();

const config = {
  user: process.env.AZURE_SQL_USER,
  password: process.env.AZURE_SQL_PASSWORD,
  server: process.env.AZURE_SQL_SERVER,
  database: process.env.AZURE_SQL_DATABASE,
  options: {
    encrypt: true,
    trustServerCertificate: true, // Change to true for local dev / self-signed certs
  },
};

sql.connect(config).then(() => {
  console.log('Connected to Azure SQL Database');
}).catch(err => {
  console.error('Connection Failed:', err);
});

const pool = new sql.ConnectionPool(config);
const poolConnect = pool.connect();

module.exports = {
  sql,
  poolConnect,
  pool
};

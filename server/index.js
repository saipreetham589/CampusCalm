const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const resultRoutes = require('./routes/results');
app.use('/api/result', resultRoutes);

app.use(cors());
app.use(express.json());

app.use('/api/auth', require('./routes/auth'));

const screeningRoutes = require('./routes/screening');
app.use('/api', screeningRoutes);

const PORT = process.env.PORT || 5050;
app.listen(PORT, () => console.log(`Auth server running on port ${PORT}`));



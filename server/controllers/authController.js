const bcrypt = require('bcryptjs');
const { pool } = require('../db');

// REGISTER USER
exports.register = async (req, res) => {
    const { charID, email, password, stevensID } = req.body;
    console.log('📥 Incoming Registration:', req.body); // <-- log here
  
    try {
      const hashedPassword = await bcrypt.hash(password, 10);
  
      const query = `
        INSERT INTO dbo.UserLogin 
          (CharID, Email, PasswordHash, StevensID, LoginDate, LoginTime, IsNewUser, IsVerified, IsActive) 
        VALUES 
          (@charID, @Email, @PasswordHash, @StevensID, GETDATE(), CONVERT(time, GETDATE()), 1, 0, 1)
      `;
  
      await pool.request()
        .input('charID', charID)
        .input('Email', email)
        .input('PasswordHash', hashedPassword)
        .input('StevensID', stevensID)
        .query(query);
  
      console.log('✅ Registered:', email);
      res.status(201).json({ message: 'Registration successful' });
    } catch (err) {
      console.error('❌ Registration Error:', err);
      res.status(500).json({ error: 'Registration failed', details: err.message });
    }
  };
  

// LOGIN USER
exports.login = async (req, res) => {
  const { email, password } = req.body;

  try {
    const result = await pool.request()
      .input('Email', email)
      .query('SELECT * FROM dbo.UserLogin WHERE Email = @Email');

    const user = result.recordset[0];
    if (!user) return res.status(400).json({ error: 'User not found' });

    const match = await bcrypt.compare(password, user.PasswordHash);
    if (!match) return res.status(400).json({ error: 'Incorrect password' });

    // Update login time
    await pool.request()
      .input('Email', email)
      .query(`UPDATE dbo.UserLogin SET LoginDate = GETDATE(), LoginTime = CONVERT(time, GETDATE()) WHERE Email = @Email`);

    res.status(200).json({
      message: 'Login successful',
      user: {
        UserID: user.UserID,
        CharID: user.CharID,
        Email: user.Email,
        IsNewUser: user.IsNewUser,
        IsVerified: user.IsVerified,
        IsActive: user.IsActive,
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Login failed', details: err.message });
  }
};

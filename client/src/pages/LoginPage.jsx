import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import logo from '../assets/CampusCalm_tran.png';
import bg from '../assets/image.jpg';
import carouselBg from '../assets/carousel-bg.jpg';
import selfAssessmentImg from '../assets/self_assement.png';
import aiSupportImg from '../assets/AI_Support.png';

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ charID: '', email: '', password: '', stevensID: '' });
  const [current, setCurrent] = useState(0);
  const navigate = useNavigate();

  const testimonials = [
    {
      quote: "Mental health is not a destination, but a process. It's about how you drive, not where you’re going.",
      author: "Noam Shpancer"
    },
    {
      quote: "You don’t have to control your thoughts. You just have to stop letting them control you.",
      author: "Dan Millman"
    },
    {
      quote: "Healing takes time, and asking for help is a courageous step.",
      author: "Mariska Hargitay"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % testimonials.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  const goNext = () => setCurrent((current + 1) % testimonials.length);
  const goPrev = () => setCurrent((current - 1 + testimonials.length) % testimonials.length);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const res = await axios.post('/api/auth/login', {
          email: form.email,
          password: form.password
        });
        localStorage.setItem('user', JSON.stringify(res.data.user));
        navigate('/home');
      } else {
        await axios.post('/api/auth/register', form);
        setIsLogin(true);
      }
    } catch (err) {
      alert(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div
      className="relative min-h-screen bg-cover bg-center overflow-y-auto"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <div className="absolute inset-0 bg-black bg-opacity-40 z-0" />

      {/* Main Content */}
      <div className="relative z-10 flex flex-col md:flex-row items-center justify-center min-h-screen px-4 pt-20">
        {/* Left Section */}
        <div className="w-full md:w-1/2 flex flex-col items-center justify-center text-center px-6">
          <div className="flex items-center justify-center gap-3 mb-4">
            <img src={logo} alt="CampusCalm Logo" className="w-16 h-16 object-contain" />
            <h1 className="text-3xl md:text-5xl font-bold text-white">CampusCalm</h1>
          </div>
          <p className="text-base md:text-lg text-white max-w-md">
            Your companion for mental wellness and emotional support.
          </p>
        </div>

        {/* Right Section (Login Box) */}
        <div className="w-full md:w-1/2 flex items-center justify-center px-6">
          <div className="bg-white w-full max-w-md rounded-xl shadow-xl p-6">
            <h2 className="text-center text-2xl font-bold text-gray-800 mb-4">
              {isLogin ? 'Welcome Back' : 'Create Your Account'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {!isLogin && (
                <>
                  <input
                    type="text"
                    placeholder="CharID (Nickname)"
                    value={form.charID}
                    onChange={(e) => setForm({ ...form, charID: e.target.value })}
                    className="w-full px-4 py-2 border rounded-md"
                    required
                  />
                  <input
                    type="text"
                    placeholder="Stevens ID"
                    value={form.stevensID}
                    onChange={(e) => setForm({ ...form, stevensID: e.target.value })}
                    className="w-full px-4 py-2 border rounded-md"
                  />
                </>
              )}
              <input
                type="email"
                placeholder="Email Address"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full px-4 py-2 border rounded-md"
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="w-full px-4 py-2 border rounded-md"
                required
              />

              <button
                type="submit"
                className="w-full bg-[#0496BE] hover:bg-[#037a9c] text-white py-2 rounded-md"
              >
                {isLogin ? 'Login' : 'Sign Up'}
              </button>
            </form>

            <div className="text-center mt-4">
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-sm text-blue-600 hover:underline"
              >
                {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Log in'}
              </button>

              {isLogin && (
                <div className="mt-3">
                  <a href="#" className="text-xs text-green-700 hover:underline">
                    Forgot password?
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Image Cards Section */}
      <div className="relative z-10 w-full bg-[#0D2B45] pt-12 pb-10">
        <div
          className="absolute inset-0 bg-cover bg-center opacity-50 blur-sm"
          style={{ backgroundImage: `url(${carouselBg})`, zIndex: -1 }}
        />
        <div className="relative z-10 max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-6">
          <img
            src={selfAssessmentImg}
            alt="Self Assessment"
            className="w-full rounded-xl shadow-md object-cover"
          />
          <img
            src={aiSupportImg}
            alt="AI Support"
            className="w-full rounded-xl shadow-md object-cover"
          />
        </div>
      </div>

      {/* Quote Carousel Section */}
      <div className="relative z-10 w-full bg-[#0D2B45] pt-10 pb-40 overflow-hidden">
        <div
          className="absolute inset-0 bg-cover bg-center opacity-60 blur-sm"
          style={{ backgroundImage: `url(${carouselBg})`, zIndex: -1 }}
        />
        <div className="relative w-full max-w-screen-xl mx-auto py-10 px-6 text-center transition-all duration-700 ease-in-out text-white">
          <p className="text-xl italic mb-4 max-w-2xl mx-auto">
            “{testimonials[current].quote}”
          </p>
          <p className="text-sm text-blue-100">— {testimonials[current].author}</p>

          <button
            onClick={goPrev}
            className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 rounded-full p-2 text-white"
          >
            ‹
          </button>
          <button
            onClick={goNext}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-40 rounded-full p-2 text-white"
          >
            ›
          </button>

          <div className="flex justify-center gap-2 mt-6">
            {testimonials.map((_, i) => (
              <span
                key={i}
                onClick={() => setCurrent(i)}
                className={`w-2.5 h-2.5 rounded-full cursor-pointer transition-all ${
                  i === current ? 'bg-white scale-125' : 'bg-white/30'
                } inline-block`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

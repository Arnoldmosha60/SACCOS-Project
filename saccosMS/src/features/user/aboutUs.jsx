/* eslint-disable no-unused-vars */
import { ArrowLeftIcon } from '@heroicons/react/24/outline';
import React from 'react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div className="flex flex-col min-h-screen bg-blue-100 pb-0 text-black">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold">KUHUSU DIT SACCOS</h1>
      </div>
      <div>AboutUs</div>
      {/* Back to Home Link */}
      <div className="text-center mt-4">
        <Link to="/" className="text-blue-600 hover:underline">
          Back to Home
        </Link>
      </div>
      {/* Footer */}
      <footer className="text-center text-gray-600 py-4 mt-8 pb-0 mb-0">
        <p>&copy; DIT SACCOS {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
};

export default About;


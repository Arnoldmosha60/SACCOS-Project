/* eslint-disable no-useless-escape */
/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable no-unused-vars */
import React, { useState } from 'react'
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';
import ImageCarousel from '../../components/Carousel/ImageCarousel';
import { Link } from 'react-router-dom';
import img1 from '../../assets/img1.jpg'
import img2 from '../../assets/img2.jpg'
import img3 from '../../assets/img3.jpg'
import img4 from '../../assets/img4.jpg'
import img5 from '../../assets/img5.jpg'
import img6 from '../../assets/img6.jpg'
import img7 from '../../assets/img7.jpg'
import img8 from '../../assets/img8.jpg'
import img9 from '../../assets/img9.jpg'
import img10 from '../../assets/img10.jpg'

const Home = () => {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <div className="bg-blue-100">
      <div className="container mx-auto px-4 py-16">
        <header className="flex justify-between items-center mb-12">
          <div className="flex items-center"> {/* Flex container for logo and text */}
            <img src="src\assets\logo.png" alt="Logo" className="h-28 w-28" /> {/* Adjust height as needed */}
            <h1 className="text-3xl font-bold text-gray-800 ml-2">DIT SACCOS LTD</h1> {/* Add margin to separate logo and text */}
          </div>
          <div className="rounded-lg overflow-hidden bg-blue-100">
            <div className="flex items-center">
              <Link to="/contactUs" className="text-gray-600 hover:text-gray-800 bg-blue-300 px-4 py-2 rounded-l-lg">Wasiliana nasi</Link>
              <Link to="/login" className="text-gray-600 hover:text-gray-800 px-4 py-2 rounded-r-lg">Member Login/Wanachama Kuingia</Link>
            </div>
          </div>
        </header>
        <div className="rounded-lg overflow-hidden shadow-lg bg-white"> {/* Change bg-gray-300 to bg-white and add shadow-lg class for elevation */}
          <header className="bg-white shadow-lg p-6 elevation-3">
            <nav className="flex justify-between items-center">
              <a href="#" className="text-xl font-bold text-black">Home</a>
              <div className="flex space-x-4">
                <Link to="/aboutUs" className="text-black hover:text-black">Kuhusu sisi</Link>
                <div
                  className="relative"
                  onMouseEnter={() => setShowDropdown(true)}
                  onMouseLeave={() => setShowDropdown(false)}
                >
                  <a href="#" className="flex items-center text-black hover:text-gray-800">
                    Uanachama
                    {showDropdown ? (
                      <ChevronUpIcon className="w-5 h-5 ml-1" />
                    ) : (
                      <ChevronDownIcon className="w-5 h-5 ml-1" />
                    )}
                  </a>
                  {showDropdown && (
                    <div className="absolute bg-blue-100 shadow-lg py-2 w-48 rounded-md z-10">
                      <Link to="/membershipRequest" className="block px-4 py-2 text-black hover:bg-gray-200">
                        Omba uanachama
                      </Link>
                      <Link to="/rulesAndRegulations" className="block px-4 py-2 text-black hover:bg-gray-200">
                        Masharti na Vigezo
                      </Link>
                    </div>
                  )}
                </div>
                <Link to="/contactUs" className="text-black hover:text-gray-800">Wasiliana nasi</Link>
              </div>
            </nav>
          </header>
          <main className="p-6 flex md:flex-col space-y-16">
            {/* Welcome Text Section */}
            <section className="flex justify-center items-center">
              {/* Image Carousel */}
              <div className="w-1/2"> {/* Adjust the width as needed */}
                {/* Add your image carousel component here */}
                <ImageCarousel images={[
                  img1, img2, img3, img4, img5, img6, img7, img8, img9, img10
                ]} />
              </div>

              {/* Text Content */}
              <div className="w-1/2 px-8"> {/* Adjust the width and padding as needed */}
                <div className="text-center">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Karibu Dar es salaam Institute of Technology Saccos</h2>
                  <p className="text-gray-600 leading-loose text-justify">
                    DIT SACCOS ni Chama cha Ushirika na Mikopo Ambacho kinanuia kuinua na kustawisha hali ya uchumi na maisha ya maisha ya wanachama wake.
                    Chama cha Ushirika cha Akiba na Mikopo DIT kilianzishwa mwaka 1998 chini ya sheria ya ushirika ya mwaka 1991 kimesajiliwa kwa nambari DSR 596 Ofisi kuu zipo Chuoni DIT.
                  </p>
                </div>
              </div>
            </section>

            {/* Call to Action Section */}
            <section className="flex justify-center items-center">
              {/* <a href="#" className="btn btn-primary"></a> */}
              <Link to='/ourServices' className='btn btn-primary'>Huduma Zetu</Link>
            </section>
          </main>
        </div>

        <footer className="text-center text-gray-600 pt-6 pb-0">
          &copy; DIT SACCOS LTD {new Date().getFullYear()}
        </footer>
      </div>
    </div>
  )
}

export default Home
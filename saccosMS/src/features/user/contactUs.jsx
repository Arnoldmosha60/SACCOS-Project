/* eslint-disable no-unused-vars */
import React from 'react'
import InputText from '../../components/Input/InputText'
import TextareaInput from '../../components/Input/TextareaInput'
import { Link } from 'react-router-dom'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'

const Contact = () => {
  const updateFormValue = ({ updateType, value }) => {
    console.log(updateType)
  }
  return (
    <div className="bg-blue-100 text-black">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-black mb-6">Wasiliana Nasi / Contact Us</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Contact Information */}
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Taarifa za mawasiliano / Contact Information</h2>
            <div className="flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M17.32 14.558c-.91-.355-1.76-.74-2.55-1.145-.815-.415-1.55-.932-2.15-1.55-.604-.62-1.054-1.326-1.35-2.08a11.952 11.952 0 0 1-.28-1.473c-.024-.21-.036-.42-.036-.63 0-.22.012-.42.037-.63a11.952 11.952 0 0 1 .28-1.474c.296-.755.746-1.46 1.35-2.08.601-.62 1.335-1.136 2.15-1.55.81-.405 1.64-.79 2.55-1.144C17.977 1.193 18.63 1 20 1v18c-1.373 0-2.026-.192-2.68-.442zM18 3.14c-1.047.345-1.95.68-2.69 1.024-.758.378-1.36.815-1.79 1.27-.436.453-.776.988-1.01 1.57a9.822 9.822 0 0 0-.23 1.203c-.024.175-.036.356-.036.543 0 .187.012.368.036.543.024.176.057.358.11.546.122.374.33.71.62 1.02.29.308.704.61 1.23.892.528.283 1.262.608 2.2.972V3.14zM16 16a28.284 28.284 0 0 1-.918 2.143c-.24.498-.646.934-1.222 1.31-.578.38-1.314.693-2.21.936-.896.245-1.942.367-3.14.367s-2.244-.122-3.14-.367c-.896-.243-1.632-.556-2.21-.937-.577-.376-.983-.812-1.222-1.31A28.284 28.284 0 0 1 4 16H0v2c0 .552.448 1 1 1h18c.552 0 1-.448 1-1v-2h-4zM7 16v-2h6v2H7z" />
              </svg>
              <span>Bibi Titi Mohamed / Morogoro Rd, Dar es salaam</span>
            </div>
            <div className="flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 3a1 1 0 0 1 1 1v6a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1zM9 3a1 1 0 0 1 1 1v6a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1zM13 3a1 1 0 0 1 1 1v6a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1zM5 13a1 1 0 0 1 1 1v1a1 1 0 0 1-2 0v-1a1 1 0 0 1 1-1zM9 13a1 1 0 0 1 1 1v1a1 1 0 0 1-2 0v-1a1 1 0 0 1 1-1zM13 13a1 1 0 0 1 1 1v1a1 1 0 0 1-2 0v-1a1 1 0 0 1 1-1z" />
              </svg>
              <span>(123) 456-7890</span>
            </div>
            <div className="flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 1c-4.4 0-8 3.6-8 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8zm0 14c-3.3 0-6-2.7-6-6s2.7-6 6-6 6 2.7 6 6-2.7 6-6 6zM11 6.2v-.1c0-.3-.1-.5-.4-.5h-1.3c-.3 0-.4.2-.4.5v.1c0 .3.1.5.4.5h1.3c.3 0 .4-.2.4-.5zm-.4 7.3c-.6 0-1.1-.5-1.1-1.1s.5-1.1 1.1-1.1c.6 0 1.1.5 1.1 1.1s-.5 1.1-1.1 1.1zm3.5-5.1c-.1-.3-.4-.4-.6-.2-.5.5-1.1.7-1.7.7s-1.2-.2-1.7-.7c-.2-.2-.5-.1-.6.2-.2.5-.4 1.1-.4 1.8 0 .3.2.5.4.7.6.5 1.3.8 2 .8s1.4-.3 2-.8c.2-.2.4-.4.4-.7 0-.7-.2-1.3-.4-1.8z" />
              </svg>
              <span>ditsaccos@gmail.com</span>
            </div>
            <div className="flex items-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 2a8 8 0 110 16 8 8 0 010-16zM5.707 10.707a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 7.414l-4.293 4.293z" clipRule="evenodd" />
              </svg>
              <span>P.O. Box 2958</span>
            </div>
          </div>
          {/* Contact Form */}
          <div className="bg-white shadow-md rounded-lg p-6 text-black">
            <form className="w-full max-w-lg text-black">
              <InputText labelTitle="Name" defaultValue="" updateFormValue={updateFormValue} placeholder="Enter fullname" className="text-black" />
              <InputText type='email' labelTitle="Email" defaultValue="" updateFormValue={updateFormValue} placeholder="****@**.com" className="bg-white" />
              <InputText labelTitle="Phone Number" defaultValue="" updateFormValue={updateFormValue} placeholder="0*********" className="bg-white" />
              <TextareaInput labelTitle="Message" defaultValue="" placeholder="Message us" updateFormValue={updateFormValue} />
              <InputText labelTitle="P.O. Box" defaultValue="" updateFormValue={updateFormValue} placeholder="Enter P.O. Box" className="bg-white" />
              <div className='pl-8 pt-12'>
                <button
                  type="button"
                  className="btn px-6 btn-sm normal-case btn-primary"
                >
                  Send
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      {/* Back to Home Link */}
      <div className="text-center mt-4">
        <Link to="/" className="text-blue-600 hover:underline">
          Back to Home
        </Link>
      </div>
      {/* Footer */}
      <footer className="text-center text-gray-600 py-4 pb-0 mb-0">
        <p>&copy; DIT SACCOS {new Date().getFullYear()}</p>
      </footer>
    </div>
  )
}

export default Contact

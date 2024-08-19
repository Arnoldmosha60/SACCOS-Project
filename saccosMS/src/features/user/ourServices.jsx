/* eslint-disable no-unused-vars */
import React from 'react'
import { Link } from 'react-router-dom';

const Services = () => {
  return (
    <div className="flex flex-col min-h-screen bg-blue-100 pb-0 text-black">
      <div className="container mx-auto px-4 py-8 flex-grow">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold">HUDUMA ZETU ZA SACCOS</h1>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="border p-4 rounded-lg shadow-lg elevation-5 bg-white">
          <h2 className="text-xl font-semibold">AKIBA YA KAWAIDA YA KUWEKA PESA NA KUTOA (DEPOSITS)</h2>
          <ul className="list-disc list-inside mt-4">
            <li>Mwanachama kuweka akiba mara kwa mara</li>
            <li>Kutoa pesa kila mara anapohitaji</li>
            <li>Weka akiba mara kwa mara ikusadie kwa mahitaji yako ya kila siku</li>
          </ul>
        </div>
        <div className="border p-4 rounded-lg shadow-lg bg-white">
          <h2 className="text-xl font-semibold">AKIBA YA LAZIMA (SAVINGS)</h2>
          <ul className="list-disc list-inside mt-4">
            <li>Kila mwezi mwanachama lazima kuweka akiba ya lazima shilingi 10,000/=</li>
            <li>Akiba hii haichukuliwi hadi kujitoa uanachama</li>
            <li>Haina ada yeyote</li>
            <li>Husaidia kudhamini mkopo</li>
            <li>Itakua inakupa riba kila mwaka</li>
            <li>Itakusaidia kuondoa usumbufu pale unapotaka kukopa na kudhamini</li>
          </ul>
        </div>
        <div className="border p-4 rounded-lg shadow-lg bg-white">
          <h2 className="text-xl font-semibold">AKIBA YA MALENGO (SPECIALIZED SAVINGS)</h2>
          <ul className="list-disc list-inside mt-4">
            <li>Kuweka akiba ya muda ya kipindi maalumu kulingana na malengo yaliopangwa</li>
            <li>Malengo yanaweza kuwa ya mwaka, miaka au miezi. Mwanachama anapanga kila mwezi anaweka kiasi kadhaa(mfano 100,000) kwa miezi 12 ili akalipe ada. Hivyo kwa mwaka ni sh 1,200,000</li>
            <li>Hupata riba mwisho wa kipindi cha kuchukua fedha za kulingana na mkataba</li>
          </ul>
        </div>
        <div className="border p-4 rounded-lg shadow-lg bg-white">
          <h2 className="text-xl font-semibold">HISA (SHARES)</h2>
          <ul className="list-disc list-inside mt-4">
            <li>Hisa ni mtaji wa mwanachama kwenye SACCOS</li>
            <li>Mwanachama anaingia SACCOS kwa hisa kianzio sh. 50,000</li>
            <li>Mwanachama anahamasishwa aongeze hisa kidogo kidogo ili aweze kupata gawio zuri kila mwaka</li>
          </ul>
        </div>
        <div className="border p-4 rounded-lg shadow-lg bg-white">
          <h2 className="text-xl font-semibold">MIKOPO (LOANS)</h2>
          <ul className="list-disc list-inside mt-4">
            <li>Mikopo inatolewa kwa mwanachama baada ya kukaa kwenye chama miezi 2 baada ya kujiunga</li>
            <li>Mikopo inatolewa kwa awamu kila mkopo mwingine unapoisha</li>
            <li>Ili kukopa mwanachama ahakikishe ana akiba 25% ya kiasi anachokopa na hisa zilizokamilika kwa mujibu wa sheria na masharti ya chama.</li>
          </ul>
        </div>
      </div>
        {/* Back to Home Link */}
        <div className="text-center mt-4">
          <Link to="/" className="text-blue-600 hover:underline">
            Back to Home
          </Link>
        </div>
      </div>
      {/* Footer */}
      <footer className="text-center text-gray-600 py-4 mt-auto">
        <p>&copy; DIT SACCOS {new Date().getFullYear()}</p>
      </footer>
    </div>
  )
}

export default Services
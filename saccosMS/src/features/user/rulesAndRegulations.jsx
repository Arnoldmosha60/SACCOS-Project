/* eslint-disable no-unused-vars */
import React from 'react';
import { Link } from 'react-router-dom';

const Regulations = () => {
    return (
        <div className="min-h-screen bg-blue-100">
            <div className="container mx-auto px-4 py-8">
                <h1 className="text-3xl font-bold text-gray-800 mb-6">Rules and Regulations</h1>

                <section className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Membership Eligibility</h2>
                    <p className="text-gray-600 leading-relaxed">
                        Here you can specify the eligibility criteria for becoming a member of your SACCO, such as age, occupation, residency, etc.
                    </p>
                </section>

                <section className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Membership Rights and Obligations</h2>
                    <p className="text-gray-600 leading-relaxed">
                        Outline the rights and obligations of your members, including their entitlements and responsibilities.
                    </p>
                </section>

                <section className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Loan Policies</h2>
                    <p className="text-gray-600 leading-relaxed">
                        Detail the loan policies of your SACCO, including eligibility criteria, loan application process, repayment terms, interest rates, etc.
                    </p>
                </section>

                <section className="mb-8">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Code of Conduct</h2>
                    <p className="text-gray-600 leading-relaxed">
                        Provide guidelines on the expected behavior and conduct of members, staff, and officials within the SACCO.
                    </p>
                </section>
                {/* Back to Home Link */}
                <div className="text-center mt-4">
                    <Link to="/" className="text-blue-600 hover:underline">
                        Back to Home
                    </Link>
                </div>
            </div>
            {/* Footer */}
            <footer className="text-center text-gray-600 py-4 pb-0 mb-0">
                <p>&copy; DIT SACCOS {new Date().getFullYear()}</p>
            </footer>
        </div>
    );
};

export default Regulations;

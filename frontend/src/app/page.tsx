import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            CV_Bot
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            AI-powered resume scanner and ranking system for HR professionals
          </p>

          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white rounded-lg p-6 shadow-md">
              <h3 className="text-xl font-semibold mb-4">Smart Job Creation</h3>
              <p className="text-gray-600">
                AI-powered questionnaire generation from job descriptions
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md">
              <h3 className="text-xl font-semibold mb-4">Resume Parsing</h3>
              <p className="text-gray-600">
                Extract and structure data from PDF/DOCX resumes with OCR fallback
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md">
              <h3 className="text-xl font-semibold mb-4">Intelligent Matching</h3>
              <p className="text-gray-600">
                Vector embeddings for semantic candidate-job matching
              </p>
            </div>
          </div>

          <div className="mt-12 space-x-4">
            <Button asChild size="lg">
              <Link href="/login">Get Started</Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/register">Sign Up</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

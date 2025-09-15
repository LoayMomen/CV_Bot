'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft, Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { candidatesAPI } from '@/lib/api';

const uploadSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  phone: z.string().optional(),
});

type UploadForm = z.infer<typeof uploadSchema>;

export default function UploadResumePage() {
  const params = useParams();
  const router = useRouter();
  const jobId = parseInt(params.id as string);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [error, setError] = useState('');
  const [uploadedCandidate, setUploadedCandidate] = useState<any>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UploadForm>({
    resolver: zodResolver(uploadSchema),
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Check file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
      if (!allowedTypes.includes(file.type)) {
        setError('Please select a PDF or Word document');
        return;
      }

      // Check file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }

      setSelectedFile(file);
      setError('');
    }
  };

  const onSubmit = async (data: UploadForm) => {
    if (!selectedFile) {
      setError('Please select a resume file');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('name', data.name);
      formData.append('email', data.email);
      if (data.phone) {
        formData.append('phone', data.phone);
      }

      const response = await candidatesAPI.uploadResume(jobId, formData);
      setUploadedCandidate(response.data);
      setUploadStatus('success');

      // Redirect after showing success message
      setTimeout(() => {
        router.push(`/dashboard/candidates/${response.data.id}`);
      }, 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload resume');
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
    }
  };

  if (uploadStatus === 'success') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <CardTitle className="text-green-900">Resume Uploaded Successfully!</CardTitle>
            <CardDescription>
              The resume has been processed and the candidate has been scored using AI analysis.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            {uploadedCandidate && (
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">{uploadedCandidate.name}</h4>
                <p className="text-sm text-gray-600 mb-2">{uploadedCandidate.email}</p>
                <div className="text-lg font-semibold text-blue-600">
                  {Math.round(uploadedCandidate.total_score * 100)}% Match Score
                </div>
              </div>
            )}
            <p className="text-sm text-gray-600">
              Redirecting to candidate details...
            </p>
            <div className="flex gap-2">
              <Button asChild className="flex-1">
                <Link href={`/dashboard/candidates/${uploadedCandidate?.id}`}>
                  View Candidate
                </Link>
              </Button>
              <Button variant="outline" asChild>
                <Link href={`/dashboard/jobs/${jobId}`}>
                  Back to Job
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center gap-4 mb-8">
            <Button variant="ghost" size="sm" asChild>
              <Link href={`/dashboard/jobs/${jobId}`}>
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Job
              </Link>
            </Button>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-500" />
                Upload Resume
              </CardTitle>
              <CardDescription>
                Upload a candidate's resume for AI-powered analysis and scoring
              </CardDescription>
            </CardHeader>

            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Candidate Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name *
                    </label>
                    <Input
                      {...register('name')}
                      placeholder="John Doe"
                    />
                    {errors.name && (
                      <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email *
                    </label>
                    <Input
                      {...register('email')}
                      type="email"
                      placeholder="john@example.com"
                    />
                    {errors.email && (
                      <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phone (Optional)
                  </label>
                  <Input
                    {...register('phone')}
                    type="tel"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>

                {/* File Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Resume File *
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                    <input
                      type="file"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileChange}
                      className="hidden"
                      id="resume-upload"
                    />
                    <label htmlFor="resume-upload" className="cursor-pointer">
                      <div className="space-y-2">
                        <FileText className="w-8 h-8 text-gray-400 mx-auto" />
                        <div className="text-sm">
                          {selectedFile ? (
                            <span className="text-blue-600 font-medium">{selectedFile.name}</span>
                          ) : (
                            <>
                              <span className="text-blue-600 font-medium">Click to upload</span>
                              <span className="text-gray-600"> or drag and drop</span>
                            </>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">
                          PDF, DOC, or DOCX up to 10MB
                        </p>
                      </div>
                    </label>
                  </div>
                  {selectedFile && (
                    <div className="mt-2 text-sm text-gray-600">
                      Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </div>
                  )}
                </div>

                {/* AI Processing Info */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-900 mb-2">AI Processing Pipeline</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Extract text and structure from resume</li>
                    <li>• Identify skills, experience, and education</li>
                    <li>• Generate semantic embeddings for matching</li>
                    <li>• Calculate weighted match score with job requirements</li>
                    <li>• Provide detailed explanation for ranking</li>
                  </ul>
                </div>

                {error && (
                  <div className="rounded-md bg-red-50 p-4 flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                )}

                <div className="flex gap-4">
                  <Button
                    type="submit"
                    disabled={isUploading || !selectedFile}
                    className="flex-1"
                  >
                    {isUploading ? (
                      <>
                        <Upload className="w-4 h-4 mr-2 animate-pulse" />
                        Processing Resume...
                      </>
                    ) : (
                      <>
                        <Upload className="w-4 h-4 mr-2" />
                        Upload & Analyze Resume
                      </>
                    )}
                  </Button>
                  <Button variant="outline" asChild>
                    <Link href={`/dashboard/jobs/${jobId}`}>Cancel</Link>
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
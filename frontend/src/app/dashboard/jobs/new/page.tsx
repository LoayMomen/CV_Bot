'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { jobsAPI } from '@/lib/api';
import Link from 'next/link';

const jobSchema = z.object({
  title: z.string().min(5, 'Job title must be at least 5 characters'),
  description: z.string().min(50, 'Job description must be at least 50 characters'),
});

type JobForm = z.infer<typeof jobSchema>;

export default function NewJobPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [createdJob, setCreatedJob] = useState<any>(null);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<JobForm>({
    resolver: zodResolver(jobSchema),
  });

  const watchedDescription = watch('description', '');

  const onSubmit = async (data: JobForm) => {
    setIsLoading(true);
    setError('');

    try {
      const response = await jobsAPI.createJob(data);
      setCreatedJob(response.data);

      // Redirect to job details after a brief delay to show success
      setTimeout(() => {
        router.push(`/dashboard/jobs/${response.data.id}`);
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setIsLoading(false);
    }
  };

  if (createdJob) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-green-600" />
            </div>
            <CardTitle className="text-green-900">Job Created Successfully!</CardTitle>
            <CardDescription>
              Your job posting has been created with AI-generated requirements and questionnaire.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="text-sm text-gray-600 mb-4">
              Redirecting to job details...
            </p>
            <Button asChild>
              <Link href={`/dashboard/jobs/${createdJob.id}`}>
                View Job Details
              </Link>
            </Button>
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
              <Link href="/dashboard">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Dashboard
              </Link>
            </Button>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-blue-500" />
                Create New Job
              </CardTitle>
              <CardDescription>
                Provide the job details and our AI will automatically generate requirements and interview questions.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title *
                  </label>
                  <Input
                    {...register('title')}
                    placeholder="e.g., Senior Software Engineer"
                    className="w-full"
                  />
                  {errors.title && (
                    <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description *
                  </label>
                  <textarea
                    {...register('description')}
                    placeholder="Describe the role, responsibilities, required skills, and qualifications. Be as detailed as possible for better AI analysis."
                    className="w-full min-h-[200px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <div className="mt-1 flex justify-between">
                    {errors.description && (
                      <p className="text-sm text-red-600">{errors.description.message}</p>
                    )}
                    <p className="text-sm text-gray-500 ml-auto">
                      {watchedDescription.length} characters
                    </p>
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-900 mb-2">What happens next?</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• AI will extract required skills and qualifications</li>
                    <li>• Automatic generation of interview questionnaire</li>
                    <li>• Smart candidate matching and ranking system</li>
                    <li>• Detailed explanations for candidate scores</li>
                  </ul>
                </div>

                {error && (
                  <div className="rounded-md bg-red-50 p-4">
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                )}

                <div className="flex gap-4">
                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1"
                  >
                    {isLoading ? (
                      <>
                        <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                        Creating Job...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4 mr-2" />
                        Create Job with AI
                      </>
                    )}
                  </Button>
                  <Button variant="outline" asChild>
                    <Link href="/dashboard">Cancel</Link>
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
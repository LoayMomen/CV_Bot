'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Upload, Users, Sparkles, Star, Clock, GraduationCap, Briefcase } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { jobsAPI, candidatesAPI } from '@/lib/api';

interface Job {
  id: number;
  title: string;
  description: string;
  requirements: any;
  questionnaire: any;
  is_active: string;
  created_at: string;
  candidate_count: number;
}

interface Candidate {
  id: number;
  name: string;
  email: string;
  total_score: number;
  status: string;
  created_at: string;
  score_breakdown: any;
}

export default function JobDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const jobId = parseInt(params.id as string);

  const [job, setJob] = useState<Job | null>(null);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (jobId) {
      fetchJobData();
    }
  }, [jobId]);

  const fetchJobData = async () => {
    try {
      const [jobResponse, candidatesResponse] = await Promise.all([
        jobsAPI.getJob(jobId),
        candidatesAPI.getCandidates(jobId)
      ]);

      setJob(jobResponse.data);
      setCandidates(candidatesResponse.data);
    } catch (err: any) {
      setError('Failed to fetch job data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'shortlisted': return 'text-green-800 bg-green-100';
      case 'reviewed': return 'text-blue-800 bg-blue-100';
      case 'rejected': return 'text-red-800 bg-red-100';
      default: return 'text-gray-800 bg-gray-100';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading job details...</div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardContent className="text-center py-8">
            <p className="text-red-600 mb-4">{error || 'Job not found'}</p>
            <Button asChild>
              <Link href="/dashboard">Back to Dashboard</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Link>
          </Button>
        </div>

        {/* Job Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <span>Created {new Date(job.created_at).toLocaleDateString()}</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  job.is_active === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {job.is_active}
                </span>
                <span className="flex items-center gap-1">
                  <Users className="w-4 h-4" />
                  {candidates.length} candidates
                </span>
              </div>
            </div>
            <Button asChild>
              <Link href={`/dashboard/jobs/${jobId}/upload`}>
                <Upload className="w-4 h-4 mr-2" />
                Upload Resume
              </Link>
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Job Description */}
            <Card>
              <CardHeader>
                <CardTitle>Job Description</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
              </CardContent>
            </Card>

            {/* AI-Generated Requirements */}
            {job.requirements && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-blue-500" />
                    AI-Generated Requirements
                  </CardTitle>
                  <CardDescription>
                    Automatically extracted from job description
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {job.requirements.skills_required?.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-1">
                        <Star className="w-4 h-4 text-red-500" />
                        Required Skills
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {job.requirements.skills_required.map((skill: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {job.requirements.skills_preferred?.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Preferred Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {job.requirements.skills_preferred.map((skill: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {job.requirements.min_experience_years > 0 && (
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-gray-500" />
                        <span>{job.requirements.min_experience_years}+ years experience</span>
                      </div>
                    )}
                    {job.requirements.education_level && (
                      <div className="flex items-center gap-2">
                        <GraduationCap className="w-4 h-4 text-gray-500" />
                        <span>{job.requirements.education_level}</span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Candidates List */}
            <Card>
              <CardHeader>
                <CardTitle>Candidates ({candidates.length})</CardTitle>
                <CardDescription>
                  Ranked by AI matching score
                </CardDescription>
              </CardHeader>
              <CardContent>
                {candidates.length === 0 ? (
                  <div className="text-center py-8">
                    <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No candidates yet</h3>
                    <p className="text-gray-600 mb-4">
                      Upload the first resume to get started with AI-powered candidate ranking
                    </p>
                    <Button asChild>
                      <Link href={`/dashboard/jobs/${jobId}/upload`}>
                        Upload First Resume
                      </Link>
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {candidates.map((candidate) => (
                      <div
                        key={candidate.id}
                        className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                        onClick={() => router.push(`/dashboard/candidates/${candidate.id}`)}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h4 className="font-medium text-gray-900">{candidate.name}</h4>
                            <p className="text-sm text-gray-600">{candidate.email}</p>
                          </div>
                          <div className="text-right">
                            <div className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(candidate.total_score)}`}>
                              {Math.round(candidate.total_score * 100)}% match
                            </div>
                          </div>
                        </div>

                        <div className="flex justify-between items-center text-sm">
                          <span className="text-gray-500">
                            Applied {new Date(candidate.created_at).toLocaleDateString()}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(candidate.status)}`}>
                            {candidate.status}
                          </span>
                        </div>

                        {candidate.score_breakdown && (
                          <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                            <div>Skills: {Math.round((candidate.score_breakdown.keyword_overlap || 0) * 100)}%</div>
                            <div>Experience: {Math.round((candidate.score_breakdown.experience_match || 0) * 100)}%</div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* AI Questionnaire */}
            {job.questionnaire && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-500" />
                    AI-Generated Interview Questions
                  </CardTitle>
                  <CardDescription>
                    Use these questions to evaluate candidates
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(job.questionnaire).map(([category, questions]: [string, any]) => (
                      <div key={category}>
                        <h4 className="font-medium text-gray-900 mb-2 capitalize">
                          {category.replace('_', ' ')}
                        </h4>
                        <div className="space-y-2">
                          {Array.isArray(questions) && questions.slice(0, 3).map((q: any, index: number) => (
                            <div key={index} className="text-sm text-gray-700 pl-4 border-l-2 border-gray-200">
                              {q.question}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
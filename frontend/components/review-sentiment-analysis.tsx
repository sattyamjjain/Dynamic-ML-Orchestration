"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { ArrowRightIcon, UploadIcon, CogIcon, DownloadIcon, MailIcon, PhoneIcon, GithubIcon, LinkedinIcon } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"

const API_BASE_URL = '/test/'

export function ReviewSentimentAnalysisComponent() {
  const [file, setFile] = useState<File | null>(null)
  const [s3Path, setS3Path] = useState("dataset/sample_reviews.csv")
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const steps = ["Ingest", "Process", "Retrieve"]

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0])
      setS3Path("")
    }
  }

  const handleS3PathChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setS3Path(event.target.value)
    setFile(null)
  }

  const handleIngest = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          Records: [
            {
              s3: {
                bucket: {
                  name: "pyverseai"
                },
                object: {
                  key: s3Path
                }
              }
            }
          ]
        }),
      })
      if (!response.ok) throw new Error('Ingest failed')
      toast({ title: "Ingest successful", description: "Data has been ingested successfully." })
      setCurrentStep(1)
      setProgress(33)
    } catch (error) {
      toast({ title: "Ingest failed", description: "There was an error ingesting the data.", variant: "destructive" })
    }
    setIsLoading(false)
  }

  const handleProcess = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          DocumentID: s3Path
        }),
      })
      if (!response.ok) throw new Error('Process failed')
      toast({ title: "Process successful", description: "Data has been processed successfully." })
      setCurrentStep(2)
      setProgress(66)
    } catch (error) {
      toast({ title: "Process failed", description: "There was an error processing the data.", variant: "destructive" })
    }
    setIsLoading(false)
  }

  const handleRetrieve = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/retrieve?document_id=${encodeURIComponent(s3Path)}`, {
        method: 'GET',
      })
      if (!response.ok) throw new Error('Retrieve failed')
      const data = await response.json()
      setResults(JSON.stringify(data, null, 2))
      toast({ title: "Retrieve successful", description: "Results have been retrieved successfully." })
      setCurrentStep(3)
      setProgress(100)
    } catch (error) {
      toast({ title: "Retrieve failed", description: "There was an error retrieving the results.", variant: "destructive" })
    }
    setIsLoading(false)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6 text-center">Dynamic ML Orchestration</h1>
      <p className="text-xl text-center mb-8">AI-Driven Review Sentiment Analysis Platform</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Project Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-4">
              Dynamic ML Orchestration is an innovative AI-driven platform designed to streamline the process of sentiment analysis for product reviews. Our serverless architecture leverages AWS services to provide a scalable, efficient, and cost-effective solution for businesses of all sizes.
            </p>
            <p>
              Key Features:
            </p>
            <ul className="list-disc list-inside mb-4">
              <li>Seamless integration with AWS S3 for data storage</li>
              <li>Advanced natural language processing for accurate sentiment analysis</li>
              <li>Real-time processing and analysis of large datasets</li>
              <li>Intuitive user interface for easy data management and result retrieval</li>
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Contact Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-center">
              <MailIcon className="mr-2" size={18} />
              <span>sattyamjain96@gmail.com</span>
            </div>
            <div className="flex items-center">
              <PhoneIcon className="mr-2" size={18} />
              <span>+91 9140675155</span>
            </div>
            <div className="flex items-center">
              <GithubIcon className="mr-2" size={18} />
              <a href="https://github.com/sattyamjjain" className="text-blue-500 hover:underline">github.com/sattyamjjain</a>
            </div>
            <div className="flex items-center">
              <LinkedinIcon className="mr-2" size={18} />
              <a href="https://www.linkedin.com/in/sattyamjain/" className="text-blue-500 hover:underline">linkedin.com/in/sattyamjjain</a>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Data Input</CardTitle>
          <CardDescription>Upload a CSV file or provide an AWS S3 path</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="s3" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-4">
              <TabsTrigger value="csv">Upload CSV</TabsTrigger>
              <TabsTrigger value="s3">AWS S3 Path</TabsTrigger>
            </TabsList>
            <TabsContent value="csv">
              <Input
                id="csv-upload"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="mb-2"
              />
              {file && <p className="text-sm text-green-600">File selected: {file.name}</p>}
            </TabsContent>
            <TabsContent value="s3">
              <Input
                id="s3-path"
                type="text"
                placeholder="s3://bucket-name/path/to/file.csv"
                value={s3Path}
                onChange={handleS3PathChange}
                className="mb-2"
              />
              {s3Path && <p className="text-sm text-green-600">S3 path provided</p>}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Analysis Workflow</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between mb-4">
            {steps.map((step, index) => (
              <div key={step} className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    index <= currentStep ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
                  }`}
                >
                  {index === 0 && <UploadIcon size={24} />}
                  {index === 1 && <CogIcon size={24} />}
                  {index === 2 && <DownloadIcon size={24} />}
                </div>
                <span className="text-sm mt-2">{step}</span>
              </div>
            ))}
          </div>
          <Progress value={progress} className="w-full mb-6" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              onClick={handleIngest}
              disabled={isLoading || currentStep !== 0 || (!file && !s3Path)}
              className="flex items-center justify-center"
            >
              <UploadIcon className="mr-2" size={18} />
              Ingest
              <ArrowRightIcon className="ml-2" size={18} />
            </Button>
            <Button
              onClick={handleProcess}
              disabled={isLoading || currentStep !== 1}
              className="flex items-center justify-center"
            >
              <CogIcon className="mr-2" size={18} />
              Process
              <ArrowRightIcon className="ml-2" size={18} />
            </Button>
            <Button
              onClick={handleRetrieve}
              disabled={isLoading || currentStep !== 2}
              className="flex items-center justify-center"
            >
              <DownloadIcon className="mr-2" size={18} />
              Retrieve
            </Button>
          </div>
        </CardContent>
      </Card>

      {results && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap bg-secondary p-4 rounded-md overflow-x-auto">
              {results}
            </pre>
          </CardContent>
        </Card>
      )}

      <footer className="mt-12 text-center text-sm text-muted-foreground">
        <p>© 2024 Dynamic ML Orchestration. All rights reserved.</p>
        <p>Developed by John Doe | SOC 2 Compliant | ISO 27001 Certified</p>
      </footer>
    </div>
  )
}
// pages/index.tsx
'use client';
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import dynamic from 'next/dynamic';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { RefreshCwIcon } from 'lucide-react';

// Import components with dynamic loading for the 3D elements
// const EarthView = dynamic(() => import('../components/EarthView'), { ssr: false });
const Dashboard = dynamic(() => import('../components/Dashboard'), { ssr: false });

// Define types
interface Position {
  x: number;
  y: number;
  z: number;
}

interface Satellite {
  id: string;
  name: string;
  orbitType: string;
  altitude: number;
  inclination: number;
  position: Position;
  lastContact: string;
  quantumKeyId: string;
  keyGeneration: string;
  status: string;
}

interface BlockchainStatus {
  blockHeight: number;
  lastBlockTime: string;
  activeValidators: number;
  transactionCount: number;
  networkStatus: string;
}

interface SystemStatus {
  satellites: Satellite[];
  blockchainData: BlockchainStatus;
  quantumKeyPool: number;
  activeChannels: number;
  systemMode: string;
  lastUpdateTime: string;
}

export default function Home() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout;

    const connectWebSocket = () => {
      try {
        ws = new WebSocket('ws://localhost:8080/ws');
        
        ws.onopen = () => {
          console.log('Connected to ThunderBird server');
          setConnected(true);
          setError(null);
        };
        
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            setStatus(data);
          } catch (e) {
            console.error('Error parsing message:', e);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setError('Connection error');
        };
        
        ws.onclose = () => {
          console.log('Disconnected from server');
          setConnected(false);
          // Try to reconnect
          reconnectTimeout = setTimeout(connectWebSocket, 5000);
        };
      } catch (error) {
        console.error('Connection failed:', error);
        setError('Failed to connect to server');
        reconnectTimeout = setTimeout(connectWebSocket, 5000);
      }
    };

    connectWebSocket();
  }, []);

  const changeMode = async (mode: string) => {
      try {
        const response = await fetch('http://localhost:8080/api/mode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ mode }),
        });
        
        if (!response.ok) {
          throw new Error(`Failed to change mode: ${response.statusText}`);
        }
  
        const data = await response.json();
        console.log('Mode changed:', data);
      } catch (error) {
        console.error('Error changing mode:', error);
        setError('Failed to change mode');
      }
    };

  return (
    <div className="min-h-screen bg-[#0f0f1a] text-white">
      <Head>
        <title>ThunderBird Quantum Space Communications</title>
        <meta name="description" content="Quantum-secured space communications system" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-6">
      {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        <h1 className="text-4xl font-bold text-center mb-6">
          ThunderBird <span className="text-[#4da8ff]">Quantum Space Communications</span>
        </h1>
        
        {!connected ? (
          <Card className="max-w-md mx-auto bg-[#1a1a2e] border-[#333]">
            <CardContent className="py-8 flex flex-col items-center justify-center space-y-4">
              <p className="text-center">Connecting to ThunderBird network...</p>
              <RefreshCwIcon className="h-8 w-8 animate-spin text-[#4da8ff]" />
            </CardContent>
          </Card>
        ) : status ? (
          <>
            <div className="flex justify-center mb-6 gap-2">
              <Button 
                variant={status.systemMode === 'realtime' ? "default" : "outline"}
                onClick={() => changeMode('realtime')}
              >
                Real-time Mode
              </Button>
              <Button 
                variant={status.systemMode === 'scenario' ? "default" : "outline"}
                onClick={() => changeMode('scenario')}
              >
                Scenario Mode
              </Button>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* <EarthView satellites={status.satellites} /> */}
              <Dashboard status={status} />
            </div>
          </>
        ) : (
          <Alert className="max-w-md mx-auto bg-[#1a1a2e] border-[#333]">
            <AlertDescription>
              Loading system data...
            </AlertDescription>
          </Alert>
        )}
      </main>

      <footer className="mt-8 py-4 border-t border-[#333] text-center text-sm text-gray-400">
        <p className="mb-2">ThunderBird Quantum-Secured Space Communications System</p>
        <p className={connected ? "text-green-500" : "text-red-500"}>
          {connected ? 
            `Connected - Last Update: ${new Date().toLocaleTimeString()}` : 
            'Disconnected - Attempting to reconnect...'}
        </p>
      </footer>
    </div>
  );
}
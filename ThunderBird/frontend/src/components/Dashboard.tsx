'use client';
import React from 'react';
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardContent 
} from '@/components/ui/card';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

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

interface DashboardProps {
  status: SystemStatus;
}

const Dashboard: React.FC<DashboardProps> = ({ status }) => {
  return (
    <Card className="flex-1 bg-[#1a1a2e] text-white max-h-[600px] overflow-y-auto">
      <CardHeader className="pb-3 border-b border-[#333] bg-[#16213e]">
        <div className="flex justify-between items-center">
          <CardTitle className="text-xl text-[#4da8ff]">System Dashboard</CardTitle>
          <div className="text-sm">
            Mode: <Badge variant={status.systemMode === 'realtime' ? 'default' : 'secondary'}>
              {status.systemMode === 'realtime' ? 'Real-time' : 'Scenario'}
            </Badge>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          <Card className="bg-[#16213e] border-0">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg text-[#4da8ff]">Quantum Security</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="my-2 text-sm flex justify-between">
                Available Keys: <span>{status.quantumKeyPool}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Active Channels: <span>{status.activeChannels}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Last Update: <span>{new Date(status.lastUpdateTime).toLocaleTimeString()}</span>
              </p>
            </CardContent>
          </Card>
          
          <Card className="bg-[#16213e] border-0">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg text-[#4da8ff]">Blockchain Status</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="my-2 text-sm flex justify-between">
                Block Height: <span>{status.blockchainData.blockHeight}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Active Validators: <span>{status.blockchainData.activeValidators}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Transactions: <span>{status.blockchainData.transactionCount}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Network: <Badge variant="default" className="capitalize">{status.blockchainData.networkStatus}</Badge>
              </p>
            </CardContent>
          </Card>
          
          <Card className="bg-[#16213e] border-0">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg text-[#4da8ff]">Satellite Fleet</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="my-2 text-sm flex justify-between">
                Total Satellites: <span>{status.satellites.length}</span>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Operational: <Badge variant="default">{status.satellites.filter(s => s.status === 'operational').length}</Badge>
              </p>
              <p className="my-2 text-sm flex justify-between">
                Limited Connection: <Badge variant="destructive">{status.satellites.filter(s => s.status === 'limited_connection').length}</Badge>
              </p>
            </CardContent>
          </Card>
        </div>
        
        <div className="mt-6">
          <h3 className="mb-4 text-lg font-semibold">Satellite Status</h3>
          <div className="rounded-md border border-[#333]">
            <Table>
              <TableHeader>
                <TableRow className="bg-[#16213e] hover:bg-[#1e2846]">
                  <TableHead className="text-[#4da8ff] font-medium">ID</TableHead>
                  <TableHead className="text-[#4da8ff] font-medium">Name</TableHead>
                  <TableHead className="text-[#4da8ff] font-medium">Altitude</TableHead>
                  <TableHead className="text-[#4da8ff] font-medium">Status</TableHead>
                  <TableHead className="text-[#4da8ff] font-medium">Last Contact</TableHead>
                  <TableHead className="text-[#4da8ff] font-medium">Key ID</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {status.satellites.map(sat => (
                  <TableRow 
                    key={sat.id} 
                    className={sat.status === 'operational' ? 'bg-green-900/10 hover:bg-green-900/20' : 'bg-orange-900/10 hover:bg-orange-900/20'}
                  >
                    <TableCell className="text-sm">{sat.id}</TableCell>
                    <TableCell className="text-sm">{sat.name}</TableCell>
                    <TableCell className="text-sm">{Math.round(sat.altitude)} km</TableCell>
                    <TableCell className="text-sm">
                      <Badge variant={sat.status === 'operational' ? 'default' : 'outline'}>
                        {sat.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm">{new Date(sat.lastContact).toLocaleTimeString()}</TableCell>
                    <TableCell className="text-sm font-mono">{sat.quantumKeyId}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default Dashboard;
'use client';

import React, { useRef, useEffect, useCallback, useState } from 'react';
import createGlobe from 'cobe';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface Position {
  x: number;
  y: number;
  z: number;
}

interface Satellite {
  id: string;
  name: string;
  position: Position;
  status: string;
}

interface EarthViewProps {
  satellites: Satellite[];
}

const EarthView: React.FC<EarthViewProps> = ({ satellites }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pointerInteracting = useRef<number | null>(null);
  const pointerInteractionMovement = useRef(0);
  const [width, setWidth] = useState(0);
  const [r, setR] = useState(0);
  let phi = 0;

  const updatePointerInteraction = (value: number | null) => {
    pointerInteracting.current = value;
    if (canvasRef.current) {
      canvasRef.current.style.cursor = value ? "grabbing" : "grab";
    }
  };

  const updateMovement = (clientX: number) => {
    if (pointerInteracting.current !== null) {
      const delta = clientX - pointerInteracting.current;
      pointerInteractionMovement.current = delta;
      setR(delta / 200);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onRender = useCallback((state: any) => {
    if (!pointerInteracting.current) {
      phi += 0.005;
    }
    state.phi = phi + r;
    state.width = width;
    state.height = width;
  }, [r, width]);

  useEffect(() => {
    const markers = satellites.map(satellite => {
      // Convert Cartesian to Spherical coordinates
      const x = satellite.position.x;
      const y = satellite.position.y;
      const z = satellite.position.z;
      
      // Calculate latitude and longitude
      const radius = Math.sqrt(x * x + y * y + z * z);
      const latitude = Math.asin(y / radius) * (180 / Math.PI);
      const longitude = Math.atan2(z, x) * (180 / Math.PI);
      
      return {
        location: [latitude, longitude] as [number, number],
        size: 0.05,
        color: satellite.status === 'operational' ? [0, 1, 0] : [1, 0, 0],
      };
    });

    if (!canvasRef.current) return;

    const onResize = () => {
      setWidth(canvasRef.current?.offsetWidth || 0);
    };
    window.addEventListener('resize', onResize);
    onResize();

    const globe = createGlobe(canvasRef.current, {
      devicePixelRatio: 2,
      width: width * 2,
      height: width * 2,
      phi: 0,
      theta: 0.3,
      dark: 1,
      diffuse: 1.2,
      mapSamples: 16000,
      mapBrightness: 6,
      baseColor: [0.3, 0.3, 0.3],
      markerColor: [0.1, 0.8, 1],
      glowColor: [0.1, 0.1, 0.3],
      markers,
      onRender,
    });

    setTimeout(() => {
      if (canvasRef.current) {
        canvasRef.current.style.opacity = '1';
      }
    });

    return () => {
      globe.destroy();
      window.removeEventListener('resize', onResize);
    };
  }, [satellites, onRender]);

  const operationalCount = satellites.filter(s => s.status === 'operational').length;

  return (
    <Card className="w-full bg-[#1a1a2e] text-white overflow-hidden">
      <CardHeader className="bg-[#16213e] border-b border-[#333] pb-3">
        <CardTitle className="text-xl text-[#4da8ff]">Earth View</CardTitle>
      </CardHeader>
      <CardContent className="p-0 relative">
        <div className="h-[600px] w-full bg-black overflow-hidden relative">
          <canvas
            ref={canvasRef}
            className="opacity-0 transition-opacity duration-500 absolute inset-0 m-auto aspect-square w-full max-w-[600px]"
            onPointerDown={(e) => updatePointerInteraction(e.clientX - pointerInteractionMovement.current)}
            onPointerUp={() => updatePointerInteraction(null)}
            onPointerOut={() => updatePointerInteraction(null)}
            onMouseMove={(e) => updateMovement(e.clientX)}
            onTouchMove={(e) => e.touches[0] && updateMovement(e.touches[0].clientX)}
          />
          <div className="absolute top-4 left-4 bg-black/70 p-3 rounded text-sm z-10">
            <p className="flex items-center justify-between mb-2">
              Active Satellites:
              <Badge variant="secondary" className="ml-2">{satellites.length}</Badge>
            </p>
            <p className="flex items-center justify-between">
              Operational:
              <Badge variant={operationalCount > 0 ? "default" : "destructive"} className="ml-2">
                {operationalCount}
              </Badge>
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EarthView;
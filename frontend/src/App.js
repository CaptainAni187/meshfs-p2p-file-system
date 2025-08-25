import React, { useState, useEffect } from 'react';

function App() {
  const [peerStatus, setPeerStatus] = useState('Not Started');
  const [peerList, setPeerList] = useState([]);

  useEffect(() => {
    // Listen for messages from the main process
    window.electronAPI.receive('from-python', (data) => {
      console.log('Received from Python:', data);
      
      if (data.type === 'PEER_STARTED') {
        setPeerStatus(`Running on port ${data.payload.port}`);
      }
      
      if (data.type === 'PEER_LIST') {
        console.log('Raw peer data:', data.payload.peers);
        console.log('Peer data type:', typeof data.payload.peers);
        console.log('Is array?', Array.isArray(data.payload.peers));
        console.log('Length:', data.payload.peers.length);
        
        // Additional debugging for each peer
        if (Array.isArray(data.payload.peers)) {
          data.payload.peers.forEach((peer, index) => {
            console.log(`Peer ${index}:`, peer, 'Type:', typeof peer);
          });
        }
        
        setPeerList(data.payload.peers);
        console.log('State updated. New peerList should be:', data.payload.peers);
      }
      
      if (data.type === 'ERROR') {
        setPeerStatus(`Error: ${data.payload.message}`);
        console.error('Error from backend:', data.payload.message);
      }
    });
  }, []);

  // Add debug logging for state changes
  useEffect(() => {
    console.log('PeerList state changed:', peerList);
  }, [peerList]);

  const startPeer = () => {
    setPeerStatus('Starting...');
    window.electronAPI.send('to-python', {
      type: 'START_PEER',
      payload: { port: 65435 }
    });
  };

  const getPeers = () => {
    console.log('Getting peers...');
    window.electronAPI.send('to-python', {
      type: 'GET_PEERS'
    });
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>MeshFS Control Panel</h1>
      <div>
        <button onClick={startPeer}>Start Peer</button>
        <p><strong>Status:</strong> {peerStatus}</p>
      </div>
      <hr />
      <div>
        <button onClick={getPeers}>Discover Peers</button>
        <h3>Connected Peers:</h3>
        
        {/* Debug info */}
        <p style={{ fontSize: '12px', color: '#666' }}>
          Debug: peerList length = {peerList.length}, 
          type = {typeof peerList}, 
          isArray = {Array.isArray(peerList).toString()}
        </p>
        
        {peerList.length > 0 ? (
          <ul>
            {peerList.map((peer, index) => (
              <li key={index}>
                {Array.isArray(peer) ? `${peer[0]}:${peer[1]}` : JSON.stringify(peer)}
              </li>
            ))}
          </ul>
        ) : (
          <p>No other peers found.</p>
        )}
      </div>
      
      {/* Raw data display for debugging */}
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f5f5f5', fontSize: '12px' }}>
        <strong>Raw peerList data:</strong>
        <pre>{JSON.stringify(peerList, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;

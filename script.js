import React, { useState, useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import Mqtt from 'react-native-mqtt';

const App = () => {
  const [temperature, setTemperature] = useState(0);
  const [motionStatus, setMotionStatus] = useState(0);

  useEffect(() => {
    // Set up MQTT client
    const client = new Mqtt.Client({ uri: 'mqtt://your_mqtt_broker_address:1883', clientId: 'clientId' });
    client.connect();

    // Subscribe to MQTT topics
    client.on('connect', () => {
      client.subscribe('room/temperature');
      client.subscribe('room/motion');
    });

    // Handle incoming MQTT messages
    client.on('message', (topic, message) => {
      if (topic === 'room/temperature') {
        setTemperature(parseFloat(message.toString()));
      } else if (topic === 'room/motion') {
        setMotionStatus(parseInt(message.toString()));
      }
    });

    // Clean up on component unmount
    return () => {
      client.disconnect();
    };
  }, []);

  return (
    <View>
      <Text>Temperature: {temperature}°C</Text>
      <Text>Motion Status: {motionStatus === 1 ? 'Motion Detected' : 'No Motion'}</Text>
      <Button title="Toggle Lights" onPress={() => {/* Add logic to publish MQTT message to control lights */}} />
    </View>
  );
};

export default App;

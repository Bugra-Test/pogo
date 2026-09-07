package com.example.virtualpogoplus;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattServer;
import android.bluetooth.BluetoothGattServerCallback;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.ParcelUuid;

import org.kivy.android.PythonActivity;

import java.util.UUID;

public class BlePeripheral {
    private BluetoothManager bluetoothManager;
    private BluetoothAdapter adapter;
    private BluetoothLeAdvertiser advertiser;
    private BluetoothGattServer gattServer;
    private AdvertiseCallback advertiseCallback;
    private BluetoothGattCharacteristic rxCharacteristic;
    private BluetoothGattCharacteristic txCharacteristic;
    private boolean running = false;

    private static final int PERMISSION_DENIED = -1;

    private boolean hasPermission(String permission) {
        return android.os.Build.VERSION.SDK_INT < 23 ||
                PythonActivity.mActivity.checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED;
    }

    public boolean start(String deviceName, String serviceUuidString,
                         String rxUuidString, String txUuidString) {
        try {
            if (android.os.Build.VERSION.SDK_INT >= 31) {
                if (!hasPermission(Manifest.permission.BLUETOOTH_ADVERTISE) ||
                    !hasPermission(Manifest.permission.BLUETOOTH_CONNECT)) {
                    return false;
                }
            }

            Context context = PythonActivity.mActivity.getApplicationContext();
            bluetoothManager = (BluetoothManager) context.getSystemService(Context.BLUETOOTH_SERVICE);
            if (bluetoothManager == null) return false;

            adapter = bluetoothManager.getAdapter();
            if (adapter == null || !adapter.isEnabled()) return false;

            advertiser = adapter.getBluetoothLeAdvertiser();
            if (advertiser == null) return false;

            adapter.setName(deviceName);

            UUID serviceUuid = UUID.fromString(serviceUuidString);
            UUID rxUuid = UUID.fromString(rxUuidString);
            UUID txUuid = UUID.fromString(txUuidString);

            BluetoothGattService service = new BluetoothGattService(
                    serviceUuid, BluetoothGattService.SERVICE_TYPE_PRIMARY);

            rxCharacteristic = new BluetoothGattCharacteristic(
                    rxUuid,
                    BluetoothGattCharacteristic.PROPERTY_WRITE |
                    BluetoothGattCharacteristic.PROPERTY_WRITE_NO_RESPONSE,
                    BluetoothGattCharacteristic.PERMISSION_WRITE);

            txCharacteristic = new BluetoothGattCharacteristic(
                    txUuid,
                    BluetoothGattCharacteristic.PROPERTY_READ |
                    BluetoothGattCharacteristic.PROPERTY_NOTIFY,
                    BluetoothGattCharacteristic.PERMISSION_READ);

            service.addCharacteristic(rxCharacteristic);
            service.addCharacteristic(txCharacteristic);

            if (gattServer != null) {
                gattServer.close();
                gattServer = null;
            }

            gattServer = bluetoothManager.openGattServer(context, new BluetoothGattServerCallback() {
                @Override
                public void onConnectionStateChange(BluetoothDevice device, int status, int newState) {
                    super.onConnectionStateChange(device, status, newState);
                }

                @Override
                public void onCharacteristicWriteRequest(BluetoothDevice device, int requestId,
                        BluetoothGattCharacteristic characteristic, boolean preparedWrite,
                        boolean responseNeeded, int offset, byte[] value) {
                    super.onCharacteristicWriteRequest(device, requestId, characteristic,
                            preparedWrite, responseNeeded, offset, value);
                    if (gattServer != null && responseNeeded) {
                        try {
                            gattServer.sendResponse(device, requestId, BluetoothGatt.GATT_SUCCESS,
                                    offset, null);
                        } catch (SecurityException ignored) { }
                    }
                }
            });

            if (gattServer == null || !gattServer.addService(service)) {
                stop();
                return false;
            }

            AdvertiseSettings settings = new AdvertiseSettings.Builder()
                    .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
                    .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
                    .setConnectable(true)
                    .setTimeout(0)
                    .build();

            AdvertiseData data = new AdvertiseData.Builder()
                    .addServiceUuid(new ParcelUuid(serviceUuid))
                    .setIncludeDeviceName(true)
                    .build();

            advertiseCallback = new AdvertiseCallback() {
                @Override
                public void onStartSuccess(AdvertiseSettings settingsInEffect) {
                    running = true;
                }

                @Override
                public void onStartFailure(int errorCode) {
                    running = false;
                }
            };

            advertiser.startAdvertising(settings, data, advertiseCallback);
            running = true;
            return true;
        } catch (SecurityException e) {
            stop();
            return false;
        } catch (Exception e) {
            stop();
            return false;
        }
    }

    public void stop() {
        try {
            if (advertiser != null && advertiseCallback != null) {
                advertiser.stopAdvertising(advertiseCallback);
            }
        } catch (Exception ignored) { }

        try {
            if (gattServer != null) gattServer.close();
        } catch (Exception ignored) { }

        gattServer = null;
        advertiser = null;
        advertiseCallback = null;
        rxCharacteristic = null;
        txCharacteristic = null;
        running = false;
    }

    public boolean isRunning() {
        return running;
    }
}

package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.LinearInterpolator;
import android.view.animation.RotateAnimation;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.TimeoutError;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.Locale;


public class MainActivity extends AppCompatActivity {

    private RequestQueue queue; //creating queue object for Volley
    double longitudeVal, latitudeVal; //stores latitude an longitude from location listener
    TextView CityStateValue, countyValue, covidCasesValue, covidDeathsValue; //will use to map onto the TextView display for the Location
    LocationManager locationManager;
    LocationListener locationListener;
    ImageButton refreshButton;
    RotateAnimation rotate = new RotateAnimation(0, 360, Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f); //rotate animation for refresh button

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //assigns queue to be a volley request
        queue = Volley.newRequestQueue(this);

        CityStateValue = (TextView) findViewById(R.id.LocationCurrText);
        countyValue = (TextView) findViewById(R.id.LocationCountyDATA);
        refreshButton = (ImageButton)findViewById(R.id.refreshLocButton);

        covidCasesValue = (TextView) findViewById(R.id.DataCasesValue);
        covidDeathsValue = (TextView) findViewById(R.id.DataDeathsValue);


        //prompts the user to enable location PERMISSION for this app
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            return;
        }else{
            // Write you code here if permission already given.
        }

        refreshButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 10, locationListener); //requests GPS updates every 5 seconds with a distance of 10 meters using locationListener

                //describes the rotation
                rotate.setDuration(750);
                rotate.setFillAfter(true);
                rotate.setRepeatCount(Animation.INFINITE); //unless we stop the button, it will rotate infinitely
                rotate.setInterpolator(new LinearInterpolator());

                refreshButton.startAnimation(rotate); //starts the rotation on the refresh button

                refreshButton.setEnabled(false); //disables the button to be clicked until a location update happens
                refreshButton.setImageAlpha(0x3F); //acts like it greys out the refresh button
            }
        });
    }

    @Override
    protected void onStart()
    {
        super.onStart();

        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE); //initiates a new location manager
        statusCheck(locationManager);

        locationListener = new MyLocationListener();

        //requests GPS updates every 5 seconds with a distance of 10 meters using locationListener
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 10, locationListener);
    }

    public void statusCheck(LocationManager locationManager) { //function to check if the user has location turned on with entire device
        if(!locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) { //checks if gps location on device is enabled
            AlertUserNoGps();
        }
    }

    private void AlertUserNoGps() { //function to prompt user to turn on device gps
        final AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("GPS is disabled for this app, enable it?")
                .setCancelable(false)
                .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    public void onClick(final DialogInterface dialog, final int id) {
                        startActivity(new Intent(android.provider.Settings.ACTION_LOCATION_SOURCE_SETTINGS));
                    }
                })
                .setNegativeButton("No", new DialogInterface.OnClickListener() {
                    public void onClick(final DialogInterface dialog, final int id) {
                        dialog.cancel();
                    }
                });
        final AlertDialog alert = builder.create();
        alert.show();
    }

    /*---------- Listener class to get coordinates ------------- */
    private class MyLocationListener implements LocationListener {

        @Override
        public void onLocationChanged(Location loc) {

            longitudeVal = loc.getLongitude();
            latitudeVal = loc.getLatitude();

            Toast.makeText(getBaseContext(),
                    "Location changed: Lat: " + latitudeVal + " Lng: "
                            + longitudeVal, Toast.LENGTH_SHORT).show();
            String longitude = "Longitude: " + longitudeVal;
            String latitude = "Latitude: " + latitudeVal;


            //account for state, county, and city at some point
            queue.cancelAll("CancelTag");//clears any prior requests from the queue
            StringRequest stringRequest = searchCountyFromCoordsRequest(latitudeVal + "", longitudeVal + "");//makes a string request, sending coords into function
            stringRequest.setTag("CancelTag");
            queue.add(stringRequest);

            locationManager.removeUpdates(locationListener); //removes location updates once the location has changed
            // cancels the animation and returns it to the start position
            rotate.cancel();
            rotate.reset();

            refreshButton.setEnabled(true); //sets the refresh button to clickable again
            refreshButton.setImageAlpha(0xFF); //sets refresh button back to original color
        }

        @Override
        public void onProviderDisabled(String provider) {}

        @Override
        public void onProviderEnabled(String provider) {}

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {}
    }

    private StringRequest searchCountyFromCoordsRequest(String latVal, String lonVal) { //uses Volley to send a string request to api w/ coords
        /* ----- Breaking each piece of the api query into individual parts ----- */
        final String FORMAT = "format=json";
        final String ZOOM = "&zoom=18";
        final String ADDRESS_DETAILS = "&addressdetails=1";
        final String URL_PREFIX = "https://nominatim.openstreetmap.org/reverse?";
        final String LATITUDE = "&lat=";
        final String LONGITUDE = "&lon=";

        String url = URL_PREFIX + FORMAT + LATITUDE + latVal + LONGITUDE + lonVal + ZOOM + ADDRESS_DETAILS;

        Log.d("reqURL", "The url is --->[" + url + "]");

        // 1st param => type of method (GET/PUT/POST/PATCH/etc)
        // 2nd param => complete url of the API
        // 3rd param => Response.Listener -> Success procedure
        // 4th param => Response.ErrorListener -> Error procedure
        return new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    // 3rd param - method onResponse lays the code procedure of success return
                    // SUCCESS
                    @Override
                    public void onResponse(String response) {
                        // try/catch block for returned JSON data
                        Log.d("Response", response);
                        try {
                            //Finds json object "address" in the query, gets the string "county" and sets the
                            //county textview to display the county resolved from coords
                            JSONObject result = new JSONObject(response).getJSONObject("address");
                            String county = result.getString("county");
                            String city = result.getString("city");
                            String state = result.getString("state");
                            CityStateValue.setText(city + ", " + state);
                            countyValue.setText(" " + county);


                            queue.cancelAll("CancelTag");//clears any prior requests from the queue
                            StringRequest covid_stringRequest = getCovidDataFromCounty(state, county);
                            covid_stringRequest.setTag("CancelTag");
                            covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                                    0,
                                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                            queue.add(covid_stringRequest);

                            
                            // catch for the JSON parsing error
                            // and catch for "city" not resolving, and "town" instead
                        } catch (JSONException e) {

                            try {
                                JSONObject result = new JSONObject(response).getJSONObject("address");
                                String county = result.getString("county");
                                String city = result.getString("town"); //heres the change
                                String state = result.getString("state");
                                CityStateValue.setText(city +", " + state);
                                countyValue.setText(" " + county);

                                queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                StringRequest covid_stringRequest = getCovidDataFromCounty(state, county);
                                covid_stringRequest.setTag("CancelTag");
                                covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                                        0,
                                        DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                queue.add(covid_stringRequest);

                                // catch for the JSON parsing error
                                // and catch for "city" and "town" not resolving, and using "village" instead
                            } catch (JSONException e2) {

                                try {
                                    JSONObject result = new JSONObject(response).getJSONObject("address");
                                    String county = result.getString("county");
                                    String city = result.getString("village"); //heres the change
                                    String state = result.getString("state");
                                    CityStateValue.setText(city +", " + state);
                                    countyValue.setText(" " + county);

                                    queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                    StringRequest covid_stringRequest = getCovidDataFromCounty(state, county);
                                    covid_stringRequest.setTag("CancelTag");
                                    covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                                            0,
                                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                    queue.add(covid_stringRequest);

                                    // catch for the JSON parsing error
                                    // and catch for "city", "town", "village" not resolving, and using "hamlet" instead
                                } catch (JSONException e3) {

                                    try {
                                        JSONObject result = new JSONObject(response).getJSONObject("address");
                                        String county = result.getString("county");
                                        String city = result.getString("hamlet"); //heres the change
                                        String state = result.getString("state");
                                        CityStateValue.setText(city +", " + state);
                                        countyValue.setText(" " + county);


                                        queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                        StringRequest covid_stringRequest = getCovidDataFromCounty(state, county);
                                        covid_stringRequest.setTag("CancelTag");
                                        //Set a retry policy in case of SocketTimeout & ConnectionTimeout Exceptions.
                                        //Volley does retry for you if you have specified the policy.
                                        //Sets retry policy to 15 seconds for this request
                                        covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                                                0,
                                                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
                                        ///////////////////////////////////////////////////////////////////////////////

                                        queue.add(covid_stringRequest);



                                        // catch for the JSON parsing error
                                    } catch (JSONException e4) {
                                        Toast.makeText(getApplicationContext(), e4.getMessage(), Toast.LENGTH_LONG).show();
                                    }

                                }

                            }

                        }
                    } // public void onResponse(String response)
                }, // Response.Listener<String>()
                new Response.ErrorListener() {
                    // 4th param - method onErrorResponse lays the code procedure of error return
                    // ERROR
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // display a simple message on the screen
                        Toast.makeText(getApplicationContext(), "Nominatim API is not responding", Toast.LENGTH_LONG).show();
                    }
                });
    }

    private StringRequest getCovidDataFromCounty(String state, final String county) { //uses Volley to send a string request to api w/ coords
        /* ----- Breaking each piece of the api query into individual parts ----- */

        final String URL_PREFIX = "http://10.0.2.2:5000/api/v1/byCounty/"; //temporary, should be able to replace with real url once have a server
                                                                                 //for now, need to make sure that localhost is started with python script, and flask is running
                                                                                 //on the android emulator, the default localhost refers to the device, and this ip refers to the laptop's localhost

        String url = URL_PREFIX + state;

        Log.d("reqURL", "The url is --->[" + url + "]");


        // 1st param => type of method (GET/PUT/POST/PATCH/etc)
        // 2nd param => complete url of the API
        // 3rd param => Response.Listener -> Success procedure
        // 4th param => Response.ErrorListener -> Error procedure
        return new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    // 3rd param - method onResponse lays the code procedure of success return
                    // SUCCESS
                    @Override
                    public void onResponse(String response) {
                        // try/catch block for returned JSON data
                        Log.d("Response", response);
                        try {
                            //Finds json object "address" in the query, gets the string "county" and sets the
                            //county textview to display the county resolved from coords

                            /*


                            //Set a retry policy in case of SocketTimeout & ConnectionTimeout Exceptions.
                            //Volley does retry for you if you have specified the policy.
                             jsonObjRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                             DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                             DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));


                             */
                            JSONObject result = new JSONObject(response).getJSONObject(county);
                            String cases = result.getString("Confirmed");
                            String deaths = result.getString("Deaths");
                            covidCasesValue.setText(cases);
                            covidDeathsValue.setText(deaths);

                            // catch for the JSON parsing error
                            // and catch for "city" not resolving, and "town" instead
                        } catch (JSONException e) {
                            Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
                        }
                    } // public void onResponse(String response)
                }, // Response.Listener<String>()
                new Response.ErrorListener() {
                    // 4th param - method onErrorResponse lays the code procedure of error return
                    // ERROR
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // display a simple message on the screen
                        if (error instanceof TimeoutError){
                            Toast.makeText(getApplicationContext(), "Local COVID API is not responding -- timeout error", Toast.LENGTH_LONG).show();
                        }
                        else {
                            Toast.makeText(getApplicationContext(), "Local COVID API is not responding", Toast.LENGTH_LONG).show();
                        }

                    }
                });
    }


    
}
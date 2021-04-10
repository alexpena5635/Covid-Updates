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

    //Creating queue object for Volley
    private RequestQueue queue;

    //Stores latitude and longitude, which will be updated from the location listener
    double longitudeVal, latitudeVal;

    //TextViews which will be mapped to text within the app which need to be updated
    TextView cityValue, stateValue, countyValue, covidCasesValue, covidDeathsValue;

    //Object declarations for locationManager/Listener
    LocationManager locationManager;
    LocationListener locationListener;

    //Button which gets mapped to the refresh Button on the main screen
    // - Defines the rotate animation which will be played later
    ImageButton refreshButton;
    RotateAnimation rotate = new RotateAnimation(0, 360, Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f); //rotate animation for refresh button

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //Sets the current view of the app to the main activity
        setContentView(R.layout.activity_main);

        //assigns queue to be a new volley request
        queue = Volley.newRequestQueue(this);

        //Assigns the TextView objects to their actual instances
        stateValue = (TextView) findViewById(R.id.locationStateCurrText);
        cityValue = (TextView) findViewById(R.id.locationCityCurrText);
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

        //This is the function which gets called when the refresh button is clicked
        refreshButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Requests GPS updates every 5 seconds with a distance of 10 meters using locationListener
                locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 10, locationListener);

                //describes the rotation of the button
                // - duration - repeat count - alpha (transparency for "greyed out" effect) - disables it so that it cannot be clicked again while rotating and checking
                rotate.setDuration(750);
                rotate.setFillAfter(true);
                rotate.setRepeatCount(Animation.INFINITE); //unless we stop the button, it will rotate infinitely
                rotate.setInterpolator(new LinearInterpolator());

                refreshButton.startAnimation(rotate); //starts the rotation on the refresh button

                refreshButton.setEnabled(false); //disables the button to be clicked until a location update happens
                refreshButton.setImageAlpha(0x3F); //acts like it greys out the refresh button

                //this will continue to rotate and be "greyed out" until locationUpdates has gone through itself
            }
        });
    }

    @Override
    protected void onStart()
    {
        super.onStart();

        //Every time te app starts, it checks the location (comes into view, first time app starts is OnCreate)
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE); //initiates a new location manager
        statusCheck(locationManager);

        locationListener = new MyLocationListener();

        //requests GPS updates every 5 seconds with a distance of 10 meters using locationListener
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 10, locationListener);
    }

    //function to check if the user has location turned on with entire device
    public void statusCheck(LocationManager locationManager) {
        //checks if gps location on device is enabled
        if(!locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
            AlertUserNoGps();
        }
    }

    //function to prompt user to turn on device gps
    private void AlertUserNoGps() {
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

            //Get the lat and long from location manager
            longitudeVal = loc.getLongitude();
            latitudeVal = loc.getLatitude();
            String longitude = "Longitude: " + longitudeVal;
            String latitude = "Latitude: " + latitudeVal;

            /*
            Toast.makeText(getBaseContext(),
                    "Location changed: Lat: " + latitudeVal + " Lng: "
                            + longitudeVal, Toast.LENGTH_SHORT).show();

             */


            //Clears any prior requests to the Volley queue, and then makes a call to the function
            // to search for a county from coordinates
            queue.cancelAll("CancelTag");
            StringRequest stringRequest = searchCountyFromCoordsRequest(latitudeVal + "", longitudeVal + "");//makes a string request, sending coords into function
            stringRequest.setTag("CancelTag");
            queue.add(stringRequest);

            //removes location updates once the location has change
            locationManager.removeUpdates(locationListener);

            // Cancels the refresh button animation and returns it to the start position
            // Also re-enables its usage, and un-"greys" it out (makes it usable and visible)
            rotate.cancel();
            rotate.reset();
            refreshButton.setEnabled(true);
            refreshButton.setImageAlpha(0xFF);
        }

        @Override
        public void onProviderDisabled(String provider) {}

        @Override
        public void onProviderEnabled(String provider) {}

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {}
    }

    //Uses Volley to send a string request to api w/ with the coordiates passed in
    private StringRequest searchCountyFromCoordsRequest(String latVal, String lonVal) {
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
                    //On a successful response to this url, this is the response sent back
                    //For our purposes, it will be a json for the nomanitm api, and for my api as well
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
                            stateValue.setText(state);
                            cityValue.setText(city + ", ");
                            countyValue.setText(" " + county);

                            //Once we know that the county was successfully parsed from the api, we can pass the county into
                            // the getCovid.. function, which will update the covid data for that county
                            queue.cancelAll("CancelTag");
                            StringRequest covid_stringRequest = getCovidDataFromCounty(state, county.substring(0, county.indexOf(" County")));
                            covid_stringRequest.setTag("CancelTag");
                            //Set a retry policy in case of SocketTimeout & ConnectionTimeout Exceptions.
                            //Volley does retry for you if you have specified the policy.
                            //Sets retry policy to 15 seconds for this request
                            covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(15000,
                                    0,
                                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                            queue.add(covid_stringRequest);

                            
                            // Catch for "city" not resolving in the returned json, checking the smaller version "town" instead
                        } catch (JSONException e) {

                            try {
                                //Finds json object "address" in the query, gets the string "county" and sets the
                                //county textview to display the county resolved from coords
                                // Also sets city to the json "town" instead
                                JSONObject result = new JSONObject(response).getJSONObject("address");
                                String county = result.getString("county");
                                String city = result.getString("town");
                                String state = result.getString("state");
                                stateValue.setText(state);
                                cityValue.setText(city + ", ");
                                countyValue.setText(" " + county);

                                //Once we know that the county was successfully parsed from the api, we can pass the county into
                                // the getCovid.. function, which will update the covid data for that county
                                queue.cancelAll("CancelTag");
                                StringRequest covid_stringRequest = getCovidDataFromCounty(state, county.substring(0, county.indexOf(" County")));
                                covid_stringRequest.setTag("CancelTag");
                                covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
                                        0,
                                        DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                queue.add(covid_stringRequest);

                                // Catch for "city" and "town" not resolving, and using "village" instead
                            } catch (JSONException e2) {

                                try {
                                    JSONObject result = new JSONObject(response).getJSONObject("address");
                                    String county = result.getString("county");
                                    String city = result.getString("village"); //heres the change
                                    String state = result.getString("state");
                                    stateValue.setText(state);
                                    cityValue.setText(city + ", ");
                                    countyValue.setText(" " + county);

                                    //Once we know that the county was successfully parsed from the api, we can pass the county into
                                    // the getCovid.. function, which will update the covid data for that county
                                    queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                    StringRequest covid_stringRequest = getCovidDataFromCounty(state, county.substring(0, county.indexOf(" County")));
                                    covid_stringRequest.setTag("CancelTag");
                                    covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
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
                                        stateValue.setText(state);
                                        cityValue.setText(city + ", ");
                                        countyValue.setText(" " + county);

                                        //Once we know that the county was successfully parsed from the api, we can pass the county into
                                        // the getCovid.. function, which will update the covid data for that county
                                        queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                        StringRequest covid_stringRequest = getCovidDataFromCounty(state, county.substring(0, county.indexOf(" County")));
                                        covid_stringRequest.setTag("CancelTag");

                                        covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
                                                0,
                                                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                        queue.add(covid_stringRequest);

                                        // Catch for ciy not resolving or any of its smaller versions
                                    } catch (JSONException e4) {
                                        try {
                                            JSONObject result = new JSONObject(response).getJSONObject("address");
                                            String county = result.getString("county");
                                            //String city = "(no value)"; //heres the change
                                            //Here we do not update the city textview, and if it was recently some other city,
                                            //it stays the same. But if it's the first location to show up, it will say "Unknown"
                                            String state = result.getString("state");
                                            stateValue.setText(state);
                                            if (cityValue.getText().length() <= 0) {
                                                cityValue.setText("Unknown, ");
                                            }
                                            countyValue.setText(" " + county);


                                            queue.cancelAll("CancelTag");//clears any prior requests from the queue
                                            StringRequest covid_stringRequest = getCovidDataFromCounty(state, county.substring(0, county.indexOf(" County")));
                                            covid_stringRequest.setTag("CancelTag");
                                            covid_stringRequest.setRetryPolicy(new DefaultRetryPolicy(25000,
                                                    0,
                                                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

                                            queue.add(covid_stringRequest);

                                            // catch for the JSON parsing error
                                        } catch (JSONException e5) {
                                            Toast.makeText(getApplicationContext(), e4.getMessage(), Toast.LENGTH_LONG).show();
                                        }
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

    //Uses volley to make a request to MY api, with the county attached to it
    //Currently, I have to run this on my localhost on my desktop, and access it through a specifc IP
    //from the android studio code bc of the way the emulator works
    //If I try and do this on my phone, it probably wont work!!!!
    private StringRequest getCovidDataFromCounty(final String state, final String county) {

        //final String URL_PREFIX = "http://10.0.2.2:5000/api/v1/byCounty/"; //temporary, should be able to replace with real url once have a server
                                                                                 //for now, need to make sure that localhost is started with python script, and flask is running
        final String URL_PREFIX = "https://covidupdatesapi3.herokuapp.com/api/v1/byCounty/";      //on the android emulator, the default localhost refers to the device, and this ip refers to the laptop's localhost

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
                            //Takes the response (json) and parses it for the object with the county name
                            //Then sets the confirmed cases and deaths textview in the app, to the values from the api
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
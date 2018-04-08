package com.example.rohitkumar.newp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

public class Forecasts extends AppCompatActivity {

    String ans=null;


    //Please change localhost name accordingly for testing
    String server_name= "http://fe81b5bf.ngrok.io/";


    TextView link;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_forecasts);
        link=(TextView) findViewById(R.id.link3);



        Spinner dynamicSpinner = (Spinner) findViewById(R.id.spinner);

        String[] items = new String[] { "Rice","Milk","Egg, Fish and Meat","Coarse Cereals","Pulses","Fruits","Wheat","Oilseeds","Fibres","All Agriculture" };

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, items);

        dynamicSpinner.setAdapter(adapter);

        dynamicSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view,
                                       int position, long id) {

                String item = parent.getItemAtPosition(position).toString();
                ans=item;
                execute(ans);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // TODO Auto-generated method stub
            }
        });
    }

    public void execute(String tmpAns)
    {

        String tmpo= server_name +"predictions?crop="+tmpAns;
        link.setText(tmpo);
    }


}

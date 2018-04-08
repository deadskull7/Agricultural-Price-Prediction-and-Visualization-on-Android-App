package com.example.rohitkumar.newp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

import com.example.rohitkumar.newp.GetPricesData;
import com.example.rohitkumar.newp.R;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void marketPrices(View view)
    {
        Intent intent= new Intent(this,GetPricesData.class);
        MainActivity.this.startActivity(intent);

    }

    public void forecast(View view)
    {
        Intent intent= new Intent(this,Forecasts.class);
        startActivity(intent);

    }

}

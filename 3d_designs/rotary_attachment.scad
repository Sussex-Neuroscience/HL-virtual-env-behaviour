/////////////////////////////////////
// code to make an adapter for a   //
// rotary encoder to fit on a wheel//
// GNU GPL 3.0 AM Chagas           //
// 23/01/2023


//sides on a cylinder
$fn=100;

//tolerance
tol = 0.1;

//wall thickness
wall_t = 2;

//rotary encoder dimensions
rot_axis_d = 4;
rot_axis_l = 10;

rot_body_d = 24;
rot_body_l = 20;

//whell connection dimensions
wheel_axis_d = 6;
wheel_axis_l = 20;

coupler_d = wheel_axis_d+2*wall_t;




wall = 4;

holH = 10;

poleDia = 25.4;
poleHei = 30;


screwDia=3.95;
nutDia = 6.91;
nutHei = 3.25;

//$fn=60;
//%cylinder(d=solD,h=solH,center=true);


//////////////////////////////////


module poleFit(){
    difference(){
    cylinder(d=poleDia+wall_t*2,h=poleHei);
        translate([0,0,-1]){
        cylinder(d=poleDia+2*tol,h=poleHei+5);
        }//end translate
    translate([-(poleDia),0,nutDia+0.5]){
        rotate([0,90,0]){
        cylinder(d=screwDia+0.5,h=poleDia+40);
        }//end rotate
    }//end translate
    }//end difference
    translate([(poleDia+wall_t*2)/2+2.5,0,nutDia-0.455]){
        nutpocket();
    }//end translate
}//end module

module nutpocket(){
    difference(){
        cube([nutHei+5,nutDia+5,nutDia+6],center=true);
        union(){
            translate([0,0,nutDia/2-2.5]){
                rotate([0,90,0]){
                    translate([0,0,-10]){
                        cylinder(d=screwDia+2*tol,h=nutHei+20);
                        }//end translate
                }//end rotate
                cube([nutHei+2*tol,nutDia+2*tol,nutDia+4+2*tol],center=true);
                }//end translate
            }//end union
        }//end differece
    }//end module




module axis_fit(){
//rotary encoder fit
difference(){
cylinder(d=coupler_d,h=rot_axis_l);
translate([0,0,0-1])
cylinder(d=rot_axis_d+2*tol,h=rot_axis_l);
    
}//end difference

translate([0,0,wheel_axis_l+rot_axis_l-0.1]){
rotate([180,0,0]){
difference(){
cylinder(d=coupler_d,h=wheel_axis_l);
translate([0,0,0-1])
cylinder(d=wheel_axis_d+2*tol,h=wheel_axis_l);
    
}//end difference
}//end rotate
}//end translate
}




module encoder_holder(){
difference(){
cylinder(d=rot_body_d+2*wall_t,h=rot_body_l);
translate([0,0,1]){
cylinder(d=rot_body_d+2*tol,h=rot_body_l+wall_t+1);
}//end translate
translate([0,-5,wall_t]){
cube([rot_body_l,10,rot_body_l+5]);
}//end translate
}//end difference
}//end module


/*
translate([(-rot_body_l-4*wall_t)/2,0,(rot_body_l+4 *wall_t)/2])
rotate([0,-90,0])
encoder_holder();

poleFit();
*/

axis_fit();


/*



translate([25,-5,0]){
cube([10,10,30]);
}//end translate

*/
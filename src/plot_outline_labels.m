
function plot_outline_labels(s,colr)
tri_lab = s.labels(s.faces);
for jj=1:length(tri_lab)
    if length(unique(tri_lab(jj,:))) ==2
        
       ind = find(tri_lab(jj,:) == mode(tri_lab(jj,:)));
       ind2 = setdiff([1,2,3],ind);
       v1=s.vertices(s.faces(jj, ind(1)),:);
       v2=s.vertices(s.faces(jj, ind2),:);
       VV1=(v1+v2)/2;
       
       v1=s.vertices(s.faces(jj, ind(2)),:);
       v2=s.vertices(s.faces(jj, ind2),:);
       VV2=(v1+v2)/2;
       VV=[VV1;VV2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color',colr);       

    end
    
    if length(unique(tri_lab(jj,:))) ==3
        
       v1=s.vertices(s.faces(jj, 1),:);
       v2=s.vertices(s.faces(jj, 2),:);
       v3=s.vertices(s.faces(jj, 3),:);
       m=(v1+v2+v3)/3;
       
       VV=[m;(v1+v2)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       
       VV=[m;(v2+v3)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       
       VV=[m;(v1+v3)/2];
       line(VV(:,1),VV(:,2),VV(:,3),'Color','r');       

    end        
    
end
end
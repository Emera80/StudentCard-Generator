
function previewPhoto() {
    const fileInput = document.getElementById('photoInput');
    const preview = document.getElementById('preview');
    const photoPreview = document.getElementById('photoPreview');
    
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            photoPreview.style.display = 'block';
            
            // Mettre aussi à jour la photo dans la carte
            document.getElementById('photoEtudiant').src = e.target.result;
        }
        
        reader.readAsDataURL(fileInput.files[0]);
    }
}

function rechercher() {
    const matricule = document.getElementById("matriculeInput").value;

    fetch(`/rechercher/?matricule=${matricule}`)
    .then(response => response.json())
    .then(data => {
        if(data.success){
            // Afficher la carte
            document.getElementById("carte").style.display = "block";
            
            // Remplir les données
            document.getElementById("matriculeValue").textContent = data.etudiant.matricule;
            document.getElementById("nom").textContent = data.etudiant.nom;
            document.getElementById("postnom").textContent = data.etudiant.postnom;
            document.getElementById("prenom").textContent = data.etudiant.prenom;
            document.getElementById("sexe").textContent = data.etudiant.sexe;
            document.getElementById("date_naissance").textContent = data.etudiant.date_naissance;
            document.getElementById("lieu_naissance").textContent = data.etudiant.lieu_naissance;
            document.getElementById("promotion").textContent = data.etudiant.promotion;
            document.getElementById("faculte").textContent = data.etudiant.faculte;
            document.getElementById("section").textContent = data.etudiant.section;
            
            // Afficher le QR code
            if(data.etudiant.qr_code_url) {
                document.getElementById("qrCode").src = data.etudiant.qr_code_url;
            }
        } else {
            alert(data.message);
            document.getElementById("carte").style.display = "none";
        }
    })
    .catch(error => {
        console.error("Erreur:", error);
        alert("Une erreur s'est produite lors de la recherche");
    });
}

// Fonction pour imprimer la carte
function imprimerCarte() {
    window.print();
}



// Déclenche le sélecteur de fichier pour la photo d'identité
function triggerPhoto(){
  const input = document.getElementById('photoInput');
  if(input){ input.click(); }
}

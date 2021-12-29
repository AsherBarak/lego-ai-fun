using System;
using UnityEngine;

namespace LEGOModelImporter
{
    public class ChangeRB :MonoBehaviour
    {
        [HideInInspector] public Rigidbody Rigidbody;
        public bool UseGravity = true;

        private void Awake()
        {
            Rigidbody = GetComponent<Rigidbody>();
        }

        private void FixedUpdate()
        {
            if (UseGravity)
            {
                Rigidbody.useGravity = false;
                Rigidbody.AddForce(Physics.gravity * (Rigidbody.mass * Rigidbody.mass));    
            }
            
        }
    }
}


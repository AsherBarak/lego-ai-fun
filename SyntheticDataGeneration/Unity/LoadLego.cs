using System;
using System.Collections;
using System.Collections.Generic;
using LEGOModelImporter;
using UnityEngine;
using Random = UnityEngine.Random;

public class LoadLego : MonoBehaviour
{
    private GameObject[] m_Models;
    [SerializeField]private int numberOfParts = 50;
    
    // Start is called before the first frame update
    void Start()
    {
     m_Models = Resources.LoadAll<GameObject>("PrefabsNew");

     for (int i = 0; i < numberOfParts; i++)
     {
         
         var tospawn = m_Models[Random.Range(0, m_Models.Length)];
         var instGO = Instantiate(tospawn,new Vector3(Random.Range(6,9),Random.Range(6,8),Random.Range(-6,-9)),Random.rotation);
       //  var Meshes = instGO.GetComponentsInChildren<MeshCollider>();
//
       //  foreach (var mesh in Meshes)
       //  {
       //      try
       //      {
       //          mesh.convex = true;
       //      }
       //      catch (Exception e)
       //      {
       //          Console.WriteLine(e);
       //          DestroyImmediate(instGO);
       //      }
       //  }
//
       //  var rig = instGO.AddComponent<Rigidbody>();
       //  rig.useGravity = false;
       //  rig.mass = 6;
       //  instGO.AddComponent<ChangeRB>();
     }
     
    }


}
